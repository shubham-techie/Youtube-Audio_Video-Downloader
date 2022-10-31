import tkinter as tk
from pytube import YouTube
import pytube
from tkinter import OptionMenu, filedialog
import os
import threading


class Youtube_downloader:
    def __init__(self, width, height):
        self.frame = tk.Tk()
        self.width = width
        self.height = height
        self.link = ""
        self.FolderName = ""
        self.display_frame_widgets()
        self.frame.mainloop()


    # ================= to get start coordinates to draw tkinter window =================
    def get_frame_start_coordinates(self,width, height):
        # getting the windows dimension
        win_width = self.frame.winfo_screenwidth()
        win_ht = self.frame.winfo_screenheight()

        # setting x,y coordinates for frame
        frame_x = int((win_width - width)/2)
        frame_y = int((win_ht - height)/2)

        return frame_x, frame_y


    # ================= to choose directory to save downloaded file ================= 
    def openDirectory(self, fileLocationLabelError):
        self.FolderName =  filedialog.askdirectory()

        if(len(self.FolderName) > 0):
            fileLocationLabelError.config(text=self.FolderName, fg="green")
        else:
            fileLocationLabelError.config(text="Please choose folder!", fg="red")


    # ================= to make error in labels text disappear after timeout ================= 
    def update_label(self, label):
        label.config(text="")


    # ================= to extract link from textbox and return Youttube() object ================= 
    def get_link_AND_YTobject(self, textbox, ytEntryError):
        self.link = textbox.get('1.0', 'end-1c') # getting text/link

        # checking whether textbox is not empty
        if len(self.link):
            # check whether it is a YT link
            try:
                yt= YouTube(self.link)
                return yt
            
            # Throw error if it some random text and not link
            except pytube.exceptions.RegexMatchError:
                ytEntryError.config(text="Error !! paste youtube link only.")
            except:
                ytEntryError.config(text="CONNECTION ERROR !!")

        # Throw error if not entered text and just clicked dwnld button      
        else:
            ytEntryError.config(text="Error !! No link")
        
        ytEntryError.after(8000, lambda : self.update_label(ytEntryError))

    
    # ================= to display dropdown of available resolutions of that particular video ================= 
    # def display_resolution(self, textbox, ytEntryError):
    #     yt = self.get_link_AND_YTobject(textbox, ytEntryError) or None

    #     if yt:
    #         yt_files = yt.streams.filter(progressive = True, file_extension='mp4').order_by('resolution').desc()

    #         resolutions = [stream.resolution for stream in yt_files]
    #         self.seleced_res= tk.StringVar()
    #         self.seleced_res.set(resolutions[0])
    #         dropdown = OptionMenu(self.frame, self.seleced_res, *resolutions)
    #         dropdown.pack()
    #         self.seleced_res = self.seleced_res.get()
    #     else:
    #         pass


    # ================= to download audio of YT file ================= 
    def download_ytaudio(self, textbox, ytEntryError, fileLocationLabelError, dwnldStatus):
        yt = self.get_link_AND_YTobject(textbox, ytEntryError) or None
        # print(yt.title)

        # perform download operation only if there is proper link in YTObject
        if yt:
            # Throw error if user has not selected directory to download file
            if len(self.FolderName)<1:
                fileLocationLabelError.config(text="Please choose folder!", fg="red")

            # perform download operation
            else:
                dwnldStatus.config(text="Downloading...")

                yt_files = yt.streams.filter(only_audio=True)   # filter only audio files
                audio_file = yt_files.first()                   # select first file
                audio_file = audio_file.download(self.FolderName) # download it
                
                # Note: file is downloaded in .mp4 audio format, so we need to change it to .mp3 format

                # separating filename along with directory and extension (i.e. mp4)
                file_name, _ = os.path.splitext(audio_file)

                # changing to .mp3 format
                try:
                    new_file_name = file_name + '.mp3'
                    os.rename(audio_file, new_file_name)

                # if file with same name exists, then append 'new_' at end
                except FileExistsError:
                    new_file_name = file_name + '_new' + '.mp3'
                    os.rename(audio_file, new_file_name)
                
                # if audio_file shows directory path, then file has been downloaded
                if audio_file:
                    dwnldStatus.config(text="Download Complete")
                else:
                    dwnldStatus.config(text="Sorry !! Audio file could not get downloaded.")

                # disappear download status after 5sec
                dwnldStatus.after(8000, lambda : self.update_label(dwnldStatus))
        else:
            pass


    # ================= to download video of YT file ================= 
    def download_ytvideo(self, textbox, ytEntryError, fileLocationLabelError, dwnldStatus):
        yt = self.get_link_AND_YTobject(textbox, ytEntryError) or None

        # perform download operation only if there is proper link in YTObject
        if yt:
            # Throw error if user has not selected directory to download file
            if len(self.FolderName)<1:
                fileLocationLabelError.config(text="Please choose folder!", fg="red")

            # perform download operation
            else:
                dwnldStatus.config(text="Downloading...")

                yt_files = yt.streams.filter(progressive = True, file_extension='mp4') # filtering
                video_file = yt_files.first()                                          # select first file
                dwnlded_file = video_file.download(self.FolderName)                    # download it

                # if dwnlded_file shows directory path, then file has been downloaded
                if dwnlded_file:
                    dwnldStatus.config(text="Download Complete")
                else:
                    dwnldStatus.config(text="Sorry !! Video could not get downloaded.")

                # disappear download status after 5sec
                dwnldStatus.after(7000, lambda : self.update_label(dwnldStatus))
        else:
            pass


    # ================= display Tkinter window ================= 
    def display_frame_widgets(self):

        # ==================================== setup to display Tkinter GUI window ==================================== 

        # set bg color
        self.frame.configure(bg='#CDCDAA')

        # set window title
        self.frame.title('Youtube AV Downloader')

        # get start coordinates to draw tkinter window
        frame_x, frame_y = self.get_frame_start_coordinates(self.width, self.height)

        # draw/display GUI app
        self.frame.geometry(f'{self.width}x{self.height}+{frame_x}+{frame_y}')

        # make sure user should not resize GUI app
        self.frame.resizable(width=False, height=False)
        


        # ==================================== display Label widgets on frame ==================================== 
        # Label to display Heading 
        TitleLabel = tk.Label(self.frame, text="Youtube Audio/Video Downloader", font=("", 15), bg="red")
        TitleLabel.pack(side=tk.TOP, ipadx=20, ipady=10, pady=(50,60))

        # Label to display prompt for input link
        ytEntry = tk.Label(self.frame, text="Please paste the youtube link here : ", bg='#CDCDAA', fg="blue",font=("Agency FB", 25))
        ytEntry.pack(pady=(0,10))

        # Label to display textbox to accept YT link
        textbox = tk.Text(self.frame, height=2, width=70)
        textbox.pack()
        
        # Label to display error if user leaves inputBox empty or if user inputs some random text
        ytEntryError = tk.Label(self.frame, text="", bg='#CDCDAA', fg="red",font=("", 11))
        ytEntryError.pack(pady=(0,10))

        # resolution_btn = tk.Button(self.frame, text="Choose Resolution : ", command=lambda :self.display_resolution(textbox, ytEntryError))
        # resolution_btn.pack(pady=(0,10), ipady=8, ipadx=10) 

        # Label to display prompt to select diretory to save downloaded file
        SaveFile = tk.Label(self.frame, text="Where to download file : ", bg='#CDCDAA', fg="blue", font=("Arial", 14))
        SaveFile.pack(pady=(0,0))
        
        # Label to display file directory or show error if not selected
        fileLocationLabelError = tk.Label(self.frame, text="", bg='#CDCDAA', fg="blue",font=("", 11))
        fileLocationLabelError.pack(pady=(0,5))

        # Label to display 
        save_Entry_btn = tk.Button(self.frame, text="Choose folder", command=lambda :self.openDirectory(fileLocationLabelError))
        save_Entry_btn.pack(pady=(0,10), ipady=8, ipadx=10)  



        # ==================================== display buttons ==================================== 

        # Button to download audio file
        # audio_download_btn = tk.Button(self.frame, text="Download audio", command=lambda : Task(self, self.download_ytaudio(textbox, ytEntryError, fileLocationLabelError, dwnldStatus)))
        audio_download_btn = tk.Button(self.frame, text="Download audio", command= threading.Thread(target=lambda : self.download_ytaudio(textbox, ytEntryError, fileLocationLabelError, dwnldStatus)).start)
        audio_download_btn.pack(side=tk.LEFT, ipady=8, ipadx=10, padx=(60,0))

        # Button to download video file
        # video_download_btn = tk.Button(self.frame, text="Download video", command= lambda : Task(self, self.download_ytvideo(textbox, ytEntryError, fileLocationLabelError, dwnldStatus)))
        video_download_btn = tk.Button(self.frame, text="Download video", command= threading.Thread(target=lambda : self.download_ytvideo(textbox, ytEntryError, fileLocationLabelError, dwnldStatus)).start)
        video_download_btn.pack(side=tk.RIGHT, ipady=8, ipadx=10, padx=(0,60))


        # Label to display download status
        dwnldStatus = tk.Label(self.frame, text="", bg='#CDCDAA', fg="green", font=("", 11))
        dwnldStatus.pack(side=tk.BOTTOM, pady=(0,10))


if __name__ == '__main__':
    yt =  Youtube_downloader(700,600)