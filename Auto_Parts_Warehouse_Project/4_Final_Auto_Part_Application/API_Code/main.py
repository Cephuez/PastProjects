import oracledb
import os
from uuid import uuid4
from fastapi import FastAPI, Header, HTTPException
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
sessions = {}

# Using env variables to load my sensitive information
def get_connection():
    return oracledb.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            dsn=os.getenv('DB_DSN'),
            config_dir='wallet',
            wallet_location= os.getenv('WALLET_PATH'),
            wallet_password=os.getenv('WALLET_PASSWORD')
        )
        

@app.get("/")
def root():
    return {"message": "Warehouse API Running"}

@app.get("/check-login")
def check_login(user_name: str, password: str):
    connection = get_connection()
    cursor = connection.cursor()
    query = """
        SELECT 1
        FROM EMPLOYEE_LOGIN
        WHERE USER_NAME = :user_name AND PASSWORD = :password
    """
    cursor.execute(query, {"user_name": user_name, "password": password})
    login_auth = cursor.fetchone()
    cursor.close()
    connection.close()

    if login_auth is None:
        return login_auth

    if user_name == "TDEMO":
        role = "admin"
    else:
        role = "demo"  
    token = str(uuid4())
    
    sessions[token] = {
        "username": user_name,
        "role": role
    }

    return {
        "success": True,
        "token": token
    }

@app.get('/check-tote')
def check_tote(tote_zone: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT PACKAGE_APPROVED_ZONE.BIN_AND_ZONE_EXISTS('PICK', :tote_zone)
        FROM DUAL
    """
    cursor.execute(query, {"tote_zone": tote_zone})
    check_tote_query = cursor.fetchall()
    cursor.close()
    connection.close()

    return check_tote_query

@app.get('/pick-list')
def get_pick_list(auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()
    query = """
        SELECT BIN_LOCATION, SUM(QUANTITY) QUANTITY
        FROM PICKS
        WHERE TIME_PICKED IS NULL
        GROUP BY BIN_LOCATION
        ORDER BY BIN_LOCATION
    """
    cursor.execute(query)
    pick_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return pick_list

@app.get('/bin-display')
def display_bin(bin_picked: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT DISTINCT ZONE_LOCATION
        FROM PICKS
        WHERE BIN_LOCATION = :bin_picked AND PICK_STATUS = 'N'
        ORDER BY ZONE_LOCATION
    """
    cursor.execute(query, {"bin_picked": bin_picked})
    bin_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return bin_list

@app.get('/load-bin-info')
def load_bin_pick_view(zone_loc: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT PK.PRODUCT_ID, SUM(PK.QUANTITY), PK.ZONE_LOCATION, P.PRODUCT_NAME
        FROM PICKS PK
        JOIN PRODUCT P 
            ON PK.PRODUCT_ID = P.PRODUCT_ID
        WHERE ZONE_LOCATION = :zone_loc AND PICK_STATUS = 'N'
        GROUP BY PK.PRODUCT_ID, PK.ZONE_LOCATION, P.PRODUCT_NAME
        ORDER BY PK.ZONE_LOCATION
    """
    cursor.execute(query, {"zone_loc": zone_loc})
    product_zone_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return product_zone_list

@app.get('/check-quantity-input')
def check_quantity_input(product_id: str, input_qty: str, bin_loc: str, zone_loc: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()
    
    query = """
        SELECT PACKAGE_PICKS.CHECK_QUANTITY_INPUT(:product_id, :input_qty, :bin_loc, :zone_loc)
        FROM DUAL
    """
    cursor.execute(query, {"product_id": product_id, "input_qty": input_qty, "bin_loc": bin_loc, "zone_loc": zone_loc})
    check_quantity_status = cursor.fetchall()
    cursor.close()
    connection.close()

    return check_quantity_status

@app.get('/process-pick')
def process_pick(product_id: str, input_qty: str, bin_loc: str, zone_loc: str, tote_zone: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    if session["role"] != "admin":
        raise HTTPException(status_code=403, detail="No permission")
    
    query = """
        BEGIN PACKAGE_PICKS.PROCESS_PICKS(:product_id, 1, :input_qty, :bin_loc, :zone_loc, 'PICK', :tote_zone);
        commit;
        END;
    """
    cursor.execute(query, {'product_id': product_id, 'input_qty': input_qty, 'bin_loc': bin_loc, 'zone_loc': zone_loc, 'tote_zone': tote_zone})
    cursor.close()
    connection.close()

@app.get('/return-updated-view')
def return_updated_view(zone_loc: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    connection = get_connection()
    cursor = connection.cursor()

    # Move the products to its new location
    query = """
        SELECT PK.PRODUCT_ID, SUM(PK.QUANTITY), PK.ZONE_LOCATION, P.PRODUCT_NAME
        FROM PICKS PK
        JOIN PRODUCT P
            ON PK.PRODUCT_ID = P.PRODUCT_ID
        WHERE ZONE_LOCATION = :zone_loc AND PICK_STATUS = 'N' 
        GROUP BY PK.PRODUCT_ID, PK.ZONE_LOCATION, P.PRODUCT_NAME 
        ORDER BY PK.ZONE_LOCATION
    """
    cursor.execute(query, {'zone_loc': zone_loc})
    updated_view = cursor.fetchall()
    cursor.close()
    connection.close()

    return updated_view

@app.get('/check-tote')
def check_tote_status(tote_zone: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT PACKAGE_APPROVED_ZONE.BIN_AND_ZONE_EXISTS('PICK', :tote_zone)
        FROM DUAL
    """
    cursor.execute(query, {'tote_zone': tote_zone})
    tote_status = cursor.fetchall()
    cursor.close()
    connection.close()

    return tote_status

@app.get('/check-empty-tote')
def check_empty_tote_status(tote_zone: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT COUNT(*)
        FROM ORDER_LIST
        WHERE ZONE = :tote_zone
    """
    cursor.execute(query, {'tote_zone': tote_zone})
    empty_tote_status = cursor.fetchall()
    cursor.close()
    connection.close()

    return empty_tote_status

@app.get('/check-valid-product')
def check_valid_product(product_id: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT COUNT(*)
        FROM PRODUCT
        WHERE TO_CHAR(PRODUCT_ID) = :product_id
    """
    cursor.execute(query, {'product_id': product_id})
    check_valid_product = cursor.fetchall()
    cursor.close()
    connection.close()

    return check_valid_product    
    # return check_quantity_status

@app.get('/check-product-count')
def check_product_count(tote_zone: str, product_id: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT COUNT(UNITS)
        FROM ORDER_LIST
        WHERE ZONE = :tote_zone AND PRODUCT_ID = :product_id
        ORDER BY PRODUCT_ID
    """

    cursor.execute(query, {'tote_zone': tote_zone, 'product_id': product_id})
    count_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return count_list

@app.get('/load-product-view')
def load_product_view(tote_zone: str, product_id: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT OL.PRODUCT_ID, COUNT(OL.UNITS), P.PRODUCT_NAME
        FROM ORDER_LIST OL
        JOIN PRODUCT P 
            ON OL.PRODUCT_ID = P.PRODUCT_ID
        WHERE OL.ZONE = :tote_zone AND OL.PRODUCT_ID = :product_id
        GROUP BY OL.PRODUCT_ID, P.PRODUCT_NAME
    """
    cursor.execute(query, {'tote_zone': tote_zone, 'product_id': product_id})
    product_view = cursor.fetchall()
    cursor.close()
    connection.close()

    return product_view

@app.get('/check-stage')
def check_stage(stage_scanned: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()
    query = """
        SELECT PACKAGE_APPROVED_ZONE.BIN_AND_ZONE_EXISTS('STAGE', :stage_scanned)
        FROM DUAL
    """
    cursor.execute(query, {"stage_scanned": stage_scanned})
    stage_status = cursor.fetchall()
    cursor.close()
    connection.close()

    return stage_status

@app.get('/move-product-to-stage')
def move_product_to_stage(product_id: str, quantity_scanned: str, tote_zone: str, stage_scanned: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    if session["role"] != "admin":
        raise HTTPException(status_code=403, detail="No permission")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        BEGIN PACKAGE_ORDER_LIST.MOVE_TOTE_TO_STAGE(:product_id, 1, :quantity_scanned, 'PICK',:tote_zone,'STAGE',:stage_scanned);
        commit;
        END;    
    """
    cursor.execute(query, {'product_id': product_id, 'quantity_scanned': quantity_scanned, 'tote_zone': tote_zone, 'stage_scanned': stage_scanned})
    cursor.close()
    connection.close()

@app.get('/updated-stage-view')
def get_updated_stage_view(tote_zone: str, product_id: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT OL.PRODUCT_ID, COUNT(OL.UNITS), P.PRODUCT_NAME
        FROM ORDER_LIST OL
        JOIN PRODUCT P
            ON OL.PRODUCT_ID = P.PRODUCT_ID
        WHERE OL.ZONE = :tote_zone AND OL.PRODUCT_ID = :product_id
        GROUP BY OL.PRODUCT_ID, P.PRODUCT_NAME 
    """
    
    cursor.execute(query, {'tote_zone': tote_zone, 'product_id': product_id})
    updated_stage_view = cursor.fetchall()
    cursor.close()
    connection.close()

    return updated_stage_view

@app.get('/check-tote-empty')
def check_tote_empty(tote_zone: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT COUNT(*)
        FROM ORDER_LIST
        WHERE ZONE = :tote_zone
    """
    
    cursor.execute(query, {'tote_zone': tote_zone})
    tote_empty_status = cursor.fetchall()
    cursor.close()
    connection.close()

    return tote_empty_status

@app.get('/get-order-ids')
def get_order_ids(auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT DISTINCT(ORDER_ID)
        FROM ORDERS_READY
        ORDER BY ORDER_ID
    """
    
    cursor.execute(query)
    order_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return order_list

@app.get('/check-tote-exist')
def check_tote_exist(box_tote: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query= """
        SELECT COUNT(*)
        FROM APPROVED_ZONE
        WHERE ZONE = :box_tote AND BIN = 'COMP'
    """
    cursor.execute(query, {'box_tote': box_tote})
    tote_count_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return tote_count_list

@app.get('/check-available-tote')
def check_available_tote(box_tote: str, order_id: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT COUNT(*)
        FROM ORDER_LIST
        WHERE ZONE = :box_tote AND ORDER_ID != :order_id
    """
    cursor.execute(query, {"box_tote": box_tote, "order_id": order_id})
    tote_count_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return tote_count_list

@app.get('/get-zone-loc-for-order')
def get_zone_loc_order(order_id: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT DISTINCT(ZONE)
        FROM ORDERS_READY
        WHERE ORDER_ID = :order_id
        ORDER BY ZONE
    """
    cursor.execute(query, {"order_id": order_id})
    order_zone_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return order_zone_list

@app.get('/get-order-scan-list')
def get_order_scan_list(order_id: str, curr_stage: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT O.PRODUCT_ID, COUNT(O.QUANTITY), P.PRODUCT_NAME
        FROM ORDERS_READY O
        JOIN PRODUCT P
            ON O.PRODUCT_ID = P.PRODUCT_ID
        WHERE O.ORDER_ID = :order_id AND O.ZONE = :curr_stage
        GROUP BY O.PRODUCT_ID, P.PRODUCT_NAME
        ORDER BY O.PRODUCT_ID 
    """
    cursor.execute(query, {"order_id": order_id, "curr_stage": curr_stage})
    order_scan_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return order_scan_list

@app.get('/check-total-product-qty')
def check_total_product_qty(order_id: str, input_product_id: str, curr_stage:str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT SUM(QUANTITY)
        FROM ORDERS_READY
        WHERE ORDER_ID = :order_id AND PRODUCT_ID = :input_product_id AND ZONE = :curr_stage     
    """
    cursor.execute(query, {"order_id": order_id, "input_product_id": input_product_id, "curr_stage": curr_stage})
    total_product_qty = cursor.fetchall()
    cursor.close()
    connection.close()

    return total_product_qty

@app.get('/move-stage-to-box')
def move_stage_to_box(order_id: str, input_product_id: str, input_qty: str, curr_stage: str, box_tote: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    if session["role"] != "admin":
        raise HTTPException(status_code=403, detail="No permission")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        BEGIN PACKAGE_ORDERS.MOVE_STAGE_TO_BOX(:order_id, :input_product_id, 4, :input_qty, 'STAGE', :curr_stage, 'COMP', :box_tote);
        commit;
        END;
    """
    cursor.execute(query, {'order_id': order_id, 'input_product_id': input_product_id, 'input_qty': input_qty, 'curr_stage': curr_stage, 'box_tote': box_tote})
    cursor.close()
    connection.close()

@app.get('/get-updated-order-view')
def get_updated_order_view(order_id: str, curr_stage: str, auth: str = Header(None)):
    session = sessions.get(auth)

    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT O.PRODUCT_ID, COUNT(O.QUANTITY), P.PRODUCT_NAME
        FROM ORDERS_READY O
        JOIN PRODUCT P
            ON O.PRODUCT_ID = P.PRODUCT_ID
        WHERE O.ORDER_ID = :order_id AND O.ZONE = :curr_stage
        GROUP BY O.PRODUCT_ID, P.PRODUCT_NAME
        ORDER BY O.PRODUCT_ID     
    """
    
    cursor.execute(query, {'order_id': order_id, 'curr_stage': curr_stage})
    updated_order_view = cursor.fetchall()
    cursor.close()
    connection.close()

    return updated_order_view   























