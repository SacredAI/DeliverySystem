Hey Sir, SO I figured out why the application wouldn't launch last time
So you need to launch the run.sh script for it to run properly without intellij (Yay Virtual enviroments)

If you don't have a program installed to run it you need to do he following
1. Goto The PortableGit Folder and open git-bash
2. Copy the file directory to the main folder of my application
3. IN bash console type the following
cd "Path/To/Folder"
4. Grant Execute permissions to the script (You probably won't need to run this command but its incase its still restricted on your system)
chmod +x ./run.sh
5. run the script
./run.sh