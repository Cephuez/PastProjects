CPU Project Guidance

This readme will help you navigate through my phases and read what parts of the code were focus on

phase1a - 	This it the beginning of coding the processes. I use a struct called Context that will be the premise of the process.
		It will keep track of important things like size of the context, if it's active, the function, and a pointer to the stack.
		The context will be stored in an array context[P1_MAXPROC] where P1_MAXPROC is a fix size number of processes.

phase1b - 	Once the context is set up, the process will have their context ID, their CPU running time, priority, and process name.
		This is where the processes will be managed throughout the CPU. It will calculate what process to run first based on priority,
		or terminate the process if it's done.

phase1c - 	In here, I code in a struct of Lock and Condition which will determine when a process will be run. Each process will be assigned a lock 
		and a condition. Each lock will be assigned a condition which will determine if they will need
		to wait for the condition to be met in order to run. I program a lock to be created, make it get locked, free it, and the name of it.
		Similar to lock, the condition will be created and freed, but in addition will have to wait for a condition met before signaling 
		the process to run.

phase1d -	I will create the handlers in here where they will be stored in an array of Interrupt Vectors. Each index will correspond to a
		an interrupt: ALARM_INT, DISK_INT, TERM_INT, etc. These handlers will be programmed to wait and abort device once asked to.

phase2a -	Once set up, I will set up Handler Array to allow user mode to call kernel mode processes. These handlers will be stored into an array
		of USLOSS_MAX_SYSCALLS where it will have a fix size of syscall methods. Each index will correspond to a handler such as initiate a process,
		make a process wait, terminate a process, and other methods more.

phase2b -	For this part, I set up a driver that would put a process to sleep for a number of seconds. I use lock to put the process to sleep once
		a the cpu's time has met a point where the process is allowed to wake up again.

phase2c -	I programmed the DiskDriver to read or write. I worked with multi-threading with processes by locking them and freeing them once
		they are ready to run again. This is where I need to make sure my threading is working well so processes do not overlap over each other.

phase2d -	For this part, I programmed in more system call handlers like in phase2a. This would allow locks to be freed, acquired, and created. 
		This is also the same for conditions. This is so user mode can call kernel to do this for the user. This will prevent user mode from
		accessing full control of kernel mode by allowing system calls to do the job for them.

phase3a -	I set up the virtual table in here by programming the number of pages, frames, blocks, what frames are freed or blocked, and more.
		I allowed pages to be allocated into the table by determining which blocks are free for memory to be stored inside.

phase3b - 	In here, I coded the frame table to determine what frames are free, the process they are associated with, and if they are free or not.
		The methods in here will be in charge of moving the pages around the table by freeing any necessary space.