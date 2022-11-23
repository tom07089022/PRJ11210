# PRJ11210
### 注意！執行此系統的電腦需有視訊鏡頭及Nvidia 20系列以前的顯示卡（Nvidia 30系列以後的顯示卡並不能使用tensorflow-gpu 1.4.0的版本）
##### NTCU-CS-PRJ-112-10
這是NTCU-CS-PRJ-112-10主要的程式碼，先將全部Code下載下來並解壓縮（建議存放在D:/）將總資料夾名稱改成tf-pose-estimation-master，環境的部分分為TFpose和Dlib  
 1. TFpose安裝：
  	* 先安裝Anaconda
  	* 開啟Anaconda Powershell Prompt
  	* 開始依次輸入以下指令：
      	* conda create -n test python=3.6 &emsp; **//建立虛擬環境，命名test（可以自己替換），指定python版本3.6**
      	* conda activate test   &emsp;   **//切換虛擬環境**
      	* pip install tensorflow-gpu==1.4.0  &emsp; **//安裝 TensorFlow**
      	* pip install keras==2.0.8         &emsp;   **//安裝 keras**
      	* pip install opencv-contrib-python  &emsp; **//安裝 OpenCV**
      	* pip install keyboard             &emsp;  **//安裝keyboard**
  	* 使用USB給的"cuda_8.0.44_win10.exe"及"cudnn-8.0-windows10-x64-v6.0.zip"配合以下網址安裝cuda和cudnn：  
  		<https://medium.com/ching-i/win10-%E5%AE%89%E8%A3%9D-cuda-cudnn-%E6%95%99%E5%AD%B8-c617b3b76deb>
2. Dlib安裝：
  	* 開啟Anaconda Powershell Prompt
  	* conda activate test            &emsp;   **//切換虛擬環境**
  	* 將USB裡的"dlib-19.7.0-cp36-cp36m-win_amd64.whl"移到你想要的位置（例如：Desktop），並且輸入以下指令：
  	* pip install C:\Users\"你的使用者名稱"\Desktop\dlib-19.7.0-cp36-cp36m-win_amd64.whl（此為"dlib-19.7.0-cp36-cp36m-win_amd64.whl"的絕對路徑）
  	* **"dlib-19.7.0-cp36-cp36m-win_amd64.whl"安裝完即可刪除**
  	* 將USB裡的"shape_predictor_68_face_landmarks.dat"放到"C:\Users\"你的使用者名稱"\anaconda3\envs\"你的虛擬環境名稱"\Lib\site-packages\dlib-19.7.0.dist-			info\"裡
  	* 更改"LRS.py"第34行的路徑為
       "C:\\Users\\"你的使用者名稱"\\anaconda3\\envs\\"你的虛擬環境名稱"\\Lib\\site-packages\\dlib-19.7.0.dist-info\\shape_predictor_68_face_landmarks.dat"
3. 目前應該就可以執行程式了
  	* 如果需要傳送檔案則要先開Server.py：
      	* 開啟Anaconda Powershell Prompt
      	* conda activate test             &emsp;   **//切換虛擬環境**
      	* python Server.py
  	* 再開啟Anaconda Powershell Prompt
  	* conda activate test                &emsp;   **//切換虛擬環境**
  	* cd 到資料夾
  	* python Final.py (需要手機) 或 -python Final_video.py (不需要手機)
  	* 如果執行 python Final.py，則電腦虛連上並且選擇名叫TEST的Project並輸入密碼（存在USB裡）：<http://iottalk2.ntcu.edu.tw:7788/connection>
  	* 且手機要也要連上並且分享手機三軸：<http://iottalk2.ntcu.edu.tw>
4. 如果途中有需要其他套件請自行下載及路徑問題可以自行修改程式碼
5. 如果還有問題可以Line或Email我們

#####ACS108120 彭冠儒 ACS108123 張正昕 ACS108129 何孟謙 合力製作
