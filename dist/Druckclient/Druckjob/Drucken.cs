using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading;
using System.Xml;
using ACAWebThumbLib;
using PDF_From_Template;


namespace Druckjob
{
    class Drucken
    {
        static void Main(string[] args)
        {
             while (true)
            {
    
                askforpdf();
                Thread.Sleep(10000);    //10 sec Warten dann weiter suchen
                
            }  
        }

        public static void print(string dateiname, string directory)
        {

            try
            {
                string sourcepdf;               //Pfade initialisieren
                string targetpdf;
                string activeDir = directory;
                string newPath = System.IO.Path.Combine(activeDir, "gedruckt");  //Unterordner erzeugen, falls vorhanden--> keine Fehlermeldung

                sourcepdf = activeDir + @"\" + dateiname;   
                targetpdf = newPath  + @"\" + dateiname;
                // Unterordner erstellen
                System.IO.Directory.CreateDirectory(newPath);
                if (File.Exists(targetpdf))
                    File.Delete(targetpdf);
                System.IO.File.Move(sourcepdf, targetpdf);          //File verschieben in den Unterordner
                string acrobat = @"C:\Program Files\Adobe\Reader 10.0\Reader\AcroRd32.exe";     //Pfad zum Acrobat Reader

                Process process = new Process();            //Process zum Drucken erzeugen
                process.StartInfo.FileName = acrobat;
                process.StartInfo.Verb = "printto";
                process.StartInfo.Arguments = "/p /s /h \"" + targetpdf + "\"";         //Pfad zum .pdf File angeben
                process.StartInfo.CreateNoWindow = true;
                process.StartInfo.RedirectStandardOutput = true;
                process.StartInfo.UseShellExecute = false;

                process.Start();
                process.CloseMainWindow(); 
             
            }
            catch (System.IO.FileNotFoundException e)
            {
                Console.WriteLine(e.Message);
            }
            
        }
        public static void askforpdf()
        {

            try
            {
                var _URL = "http://10.0.0.2:8000/einsatzfax";
                System.Net.WebClient Client = new WebClient();
                Stream strm = Client.OpenRead(_URL);
                StreamReader sr = new StreamReader(strm);
                string line;
                string XmlString = "";
                do
                {
                    line = sr.ReadLine();
                    XmlString = XmlString + line;
                    
                }
                while (line != null);
                strm.Close();
                
                using (XmlReader reader = XmlReader.Create(new StringReader(XmlString)))
                {
                    if (reader.ReadToFollowing("id"))
                    {   
                        var einsatzid = reader.ReadElementContentAsInt();
                        reader.ReadToFollowing("ausgedruckt");
                        if (reader.ReadElementContentAsString() == "False")
                        {
                            downlaodpdf(einsatzid);
                        }
                    }
                }
                
              
            }
            catch (Exception _Exception)
            {
                // Error
                Console.WriteLine("Exception caught in process: {0}", _Exception.ToString());
            }
            
        }

        public static void downlaodpdf(int pdfid)
        {
            
            try
        	{
               
                var _URL = "http://10.0.0.2:8000/einsatzfax/pdf/" + pdfid ;
                var _SaveAs = @"C:\Users\Christoph\Desktop\Druckjob\einsatz\einsatz" + pdfid +".pdf";
       	        System.Net.WebClient _WebClient = new System.Net.WebClient();
        	    // Downloads the resource with the specified URI to a local file.
        	    _WebClient.DownloadFile(_URL, _SaveAs);
                setausgedruckttrue(pdfid);
                screenshot(pdfid);
                addmaptopdf(pdfid);
                print("einsatz" + pdfid + ".pdf", @"C:\Users\Christoph\Desktop\Druckjob\einsatz");
        	}
        	catch (Exception _Exception)
        	{
        	        // Error
        	        Console.WriteLine("Exception caught in process: {0}", _Exception.ToString());
        	}
         
        }

        public static void setausgedruckttrue(int pdfid)
        {
            var _URL = "http://10.0.0.2:8000/einsatzfax/pdf/ausgedruckt/" + pdfid;
            WebRequest webRequest = WebRequest.Create(_URL);
            WebResponse webResponse = webRequest.GetResponse();
          
            webResponse.Close();
        }


        static void addmaptopdf(int pdfid)
        {

            try
            {
                var TemplateFile = @"C:\Users\Christoph\Desktop\Druckjob\einsatz\einsatz" + pdfid + ".pdf";

                var pdfFromTemplateHelper = PDFFromTemplateHelper.LoadPdfDocumentFromTemplate(TemplateFile);



                //Y-Position is offset from the bottom of the document!
                var pictureStream = File.OpenRead(@"C:\Users\Christoph\Desktop\Druckjob\einsatz\image.jpg");
                var absolutPosition = new PDFFromTemplateHelper.AbsolutPosition(0, 0);
                pdfFromTemplateHelper.AddPictureInPdfDocument(pictureStream, absolutPosition);
                var memoryStream = pdfFromTemplateHelper.CloseDocumentAndReturnStream();
                SaveMemoryStream(memoryStream, TemplateFile);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }
        }

        public static void SaveMemoryStream(MemoryStream ms, string fileName)
        {
            try
            {
                var outStream = File.OpenWrite(fileName);
                ms.WriteTo(outStream);
                outStream.Flush();
                outStream.Close();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }
        }

        public static void webscreenshot(int gmapid)
        {
            var _URL = "http://10.0.0.2:8000/gmap/" + gmapid;
            string image = @"C:\Users\Christoph\Desktop\Druckjob\einsatz\imageneu2.jpg";
            WebsitesScreenshot.WebsitesScreenshot _Obj;
            _Obj = new WebsitesScreenshot.WebsitesScreenshot();
            WebsitesScreenshot.WebsitesScreenshot.Result _Result;
            _Result = _Obj.CaptureWebpage(_URL);
            if (_Result == WebsitesScreenshot.WebsitesScreenshot.Result.Captured)
            {
                _Obj.ImageFormat = WebsitesScreenshot.
                    WebsitesScreenshot.ImageFormats.JPG;
                _Obj.SaveImage(image);
            }
            _Obj.Dispose();
        }

        public static void screenshot(int gmapid)
        {
            System.Diagnostics.Process process1;
            process1 = new System.Diagnostics.Process();

            var Programmpfad = @"C:\Siteshoter\Siteshoter.exe ";
            var urlcommand = "/URL http://10.0.0.2:8000/gmap/" + gmapid +" /Filename ";
            var file = @"""C:\Users\Christoph\Desktop\Druckjob\einsatz\image.jpg""";
            var options = " /DisableScrollBars 1 /BrowserWidth 596 /BrowserHeight 520";
            ProcessStartInfo _info =
              new ProcessStartInfo("cmd", @"/C " + Programmpfad + urlcommand + file + options );

            // The following commands are needed to redirect the
            // standard output.  This means that it will be redirected
            // to the Process.StandardOutput StreamReader.
            _info.RedirectStandardOutput = true;

            // Set UseShellExecute to false.  This tells the process to run
            // as a child of the invoking program, instead of on its own.
            // This allows us to intercept and redirect the standard output.
            _info.UseShellExecute = false;

            // Set CreateNoWindow to true, to supress the creation of
            // a new window
            _info.CreateNoWindow = true;

            // Create a process, assign its ProcessStartInfo and start it
            Process _p = new Process();
            _p.StartInfo = _info;
            _p.Start();

            // Capture the results in a string
            string _processResults = _p.StandardOutput.ReadToEnd();

            // Close the process to release system resources
            _p.Close();

        }

    }
}
