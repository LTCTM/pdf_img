# pdf_img
一个界面不会卡的小工具，支持PDF拆成小图片、小图片合成PDF。
选择文件夹，自动获取里面的图片文件并在外面生成{文件夹名.pdf}。支持文件夹嵌套。
例如：

root
-A
--1.png
--2.png
--B
---3.png
---4.png
---C
----5.png
----6.png

选择A进行合成，会在root文件夹里生成：
A.pdf       #包含1.png和2.png
A.B.Pdf     #包含3.png和4.png
A.B.C.pdf   #包含5.png和6.png
