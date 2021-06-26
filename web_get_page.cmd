date /t >> C:\Users\admin\Documents\coronavirus\web_get_page_load.out
time /t >> C:\Users\admin\Documents\coronavirus\web_get_page_load.out

cd C:\Users\admin\Documents\coronavirus

echo "Creating webpages with web_get_page3.py " 			>> C:\Users\admin\Documents\coronavirus\web_get_page_load.out

python web_get_page3.py 						>> C:\Users\admin\Documents\coronavirus\web_get_page_load.out

echo "Feeding mysql database with mysql_toolkit.py " 			>> C:\Users\admin\Documents\coronavirus\web_get_page_load.out

python mysql_toolkit.py 						> mysql_toolkit.out

echo "Creating images for webpages with plots_coronavirus.py " 		>> C:\Users\admin\Documents\coronavirus\web_get_page_load.out

python plots_coronavirus.py 						>> C:\Users\admin\Documents\coronavirus\web_get_page_load.out

echo "Feeding besada.com pages and images and data files with WinSCP " 	>> C:\Users\admin\Documents\coronavirus\web_get_page_load.out

"C:\Program Files (x86)\WinSCP\winscp.com" /ini=nul /script=C:\Users\admin\Documents\coronavirus\winscp_ftp_to_besadacom.txt



date /t >> C:\Users\admin\Documents\coronavirus\web_get_page_load.out
time /t >> C:\Users\admin\Documents\coronavirus\web_get_page_load.out