using System.IO;
using iTextSharp.text;
using iTextSharp.text.pdf;

namespace PDF_From_Template
{
    public class PDFFromTemplateHelper
    {
        private class PdfDocument
        {
            public PdfStamper PDFStamper;
            public AcroFields PDFFields;
            public MemoryStream MemoryStream;
        }
        public class AbsolutPosition
        {
            public int X { get; set; }
            public int Y { get; set; }

            public AbsolutPosition( int x, int y )
            {
                X = x;
                Y = y;
            }
        }
        public class Table
        {

            public enum Alignment
            {
                Left = 0,
                Center = 1,
                Right = 2,
                TableDefaults
            }
            public class Cell
            {

                public Phrase Phrase { get; set; }
                public Alignment Align { get; set; }

                public Cell( Phrase phrase, Alignment alignment )
                {
                    Align = alignment;
                    Phrase = phrase;
                }
                public Cell( Phrase phrase )
                {
                    Align = Alignment.TableDefaults;
                    Phrase = phrase;
                }
                public Cell()
                {
                    Align = Alignment.Left;
                    Phrase = new Phrase();
                }
            }

            public int ColsCount { get; private set; }
            public int RowsCount { get; private set; }
            public float[ ] RelativeColumnWidths { get; set; }
            public Alignment Align { get; set; }
            private Cell[,] Cells { get; set; }


            public Table( int cols, int rows )
            {
                Cells = new Cell[cols, rows];
                ColsCount = cols;
                RowsCount = rows;
                Align = Alignment.Left;
                InitRelativeColumnWidths( cols );
            }

            public Table( int cols, int rows, Alignment align )
            {
                Cells = new Cell[cols, rows];
                ColsCount = cols;
                RowsCount = rows;
                Align = align;
                InitRelativeColumnWidths( cols );
            }

            private void InitRelativeColumnWidths( int cols )
            {
                RelativeColumnWidths = new float[cols];
                for ( var i = 0; i < cols; i++ )
                    RelativeColumnWidths[i] = 1;
            }

            public void SetCell( int col, int row, Phrase phrase, Alignment alignment )
            {
                Cells[col, row] = new Cell( phrase, alignment );
            }

            public void SetCell( int col, int row, Phrase phrase )
            {
                Cells[col, row] = new Cell( phrase );
            }

            public void SetCell( int col, int row, Cell cell )
            {
                Cells[col, row] = cell;
            }

            public void SetCell( int col, int row, string text )
            {
                Cells[col, row] = new Cell( new Phrase( text ) );
            }

            public Cell GetCell( int col, int row )
            {
                var cell = Cells[col, row] ?? new Cell();
                if ( cell.Align == Alignment.TableDefaults ) cell.Align = Align;
                return cell;
            }
        }
        private class TargetContainerDetails
        {
            public float Left { get; private set; }
            public float Top { get; private set; }
            public float Width { get; private set; }
            public float Height { get; private set; }
            public int Page { get; private set; }

            public TargetContainerDetails( AcroFields.FieldPosition fieldPosition )
            {
                Left = fieldPosition.position.Left;
                Top = fieldPosition.position.Top;
                Width = fieldPosition.position.Width;
                Height = fieldPosition.position.Height;
                Page = fieldPosition.page;
            }
        }


        private readonly PdfDocument _pdfDocument;

        private PDFFromTemplateHelper( PdfDocument pdfDocument )
        {
            _pdfDocument = pdfDocument;
        }

        public static PDFFromTemplateHelper LoadPdfDocumentFromTemplate( string pathToPdfTemplate )
        {
            var pdfDocument = CreatePDFDocument( pathToPdfTemplate );
            return new PDFFromTemplateHelper( pdfDocument );
        }

        public void SetPDFFieldValueInPdfDocument( string pdfFieldName, string value )
        {
            _pdfDocument.PDFFields.SetField( pdfFieldName, value );
        }

        public void SetPDFFieldValueInPdfDocument( string pdfFieldName, string value, string display )
        {
            _pdfDocument.PDFFields.SetField( pdfFieldName, value, display );
        }

        public void AddPictureInPdfDocument( Stream inputImageStream, AbsolutPosition absolutPosition )
        {
            var pdfContentByte = _pdfDocument.PDFStamper.GetOverContent( 1 );

            var image = Image.GetInstance( inputImageStream );
            image.SetAbsolutePosition( absolutPosition.X, absolutPosition.Y );
            pdfContentByte.AddImage( image );
        }

        public void AddTableInPdfDocument( string tableIdentifier, Table table )
        {
            var fieldsInTemplate = _pdfDocument.PDFFields.GetFieldPositions( tableIdentifier );
            var targetContainerDetails = new TargetContainerDetails( fieldsInTemplate[0] );

            var pdfContent = _pdfDocument.PDFStamper.GetOverContent( targetContainerDetails.Page );

            pdfContent.CreateTemplate( targetContainerDetails.Width, targetContainerDetails.Height );
            var pdfTable = GetPdfTable( targetContainerDetails.Width, table );

            pdfTable.WriteSelectedRows( 0, 50, targetContainerDetails.Left, targetContainerDetails.Top, pdfContent );
        }

        public MemoryStream CloseDocumentAndReturnStream()
        {
            DisableFieldsForEditing();
            ClosePdfDocument();
            return _pdfDocument.MemoryStream;
        }

        #region Private Helper

        private static PdfDocument CreatePDFDocument( string templateFileName )
        {
            var templateFileStream = new FileStream( templateFileName, FileMode.Open );
            var outputStream = new MemoryStream();
            var pdfStamper = GetPDFStamper( templateFileStream, outputStream );
            templateFileStream.Close();


            return new PdfDocument
            {
                PDFStamper = pdfStamper,
                MemoryStream = outputStream,
                PDFFields = pdfStamper.AcroFields
            };
        }

        private static PdfStamper GetPDFStamper( FileStream templateFileStream, MemoryStream outputStream )
        {
            var pdfReader = GetPDFReader( templateFileStream );
            var pdfStamper = InitPDFStamper( pdfReader, outputStream );
            pdfReader.Close();
            return pdfStamper;
        }

        private static PdfReader GetPDFReader( FileStream templateFileStream )
        {
            return new PdfReader( templateFileStream );
        }

        private static PdfStamper InitPDFStamper( PdfReader pdfReader, MemoryStream outputStream )
        {
            var pdfStamper = new PdfStamper( pdfReader, outputStream );
            pdfStamper.Writer.CloseStream = false;
            return pdfStamper;
        }


        private static PdfPTable GetPdfTable( float width, Table table )
        {
            var pdfTable = new PdfPTable( table.ColsCount ) { TotalWidth = width };
            
            pdfTable.SetWidths( table.RelativeColumnWidths );
            SetColumnValues( table, pdfTable );
            return pdfTable;
        }

        private static void SetColumnValues( Table table, PdfPTable pdfTable )
        {
            for ( var row = 0; row < table.RowsCount; row++ )
                for ( var col = 0; col < table.ColsCount; col++ )
                {
                    var cell = table.GetCell( col, row );
                    var pdfPCell = new PdfPCell( cell.Phrase ) { HorizontalAlignment = (int) cell.Align };
                    pdfTable.AddCell( pdfPCell );
                }
        }


        private void DisableFieldsForEditing()
        {
            //Disable Fields - not editable anymore
            _pdfDocument.PDFStamper.FormFlattening = true;
        }

        private void ClosePdfDocument()
        {
            _pdfDocument.PDFStamper.Close();
            _pdfDocument.MemoryStream.Position = 0;
        }


        #endregion
    }
}
