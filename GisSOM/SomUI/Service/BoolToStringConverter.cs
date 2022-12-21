using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Data;

namespace SomUI.Service
{
    /// <summary>
    /// Valueconverter for converting Bool to  string
    /// </summary>
    public class BoolToStringConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            switch (value)
            {
                case false:
                    return "false";
                case true:
                    return "true";
                case "0":
                    return "true";
                case "1":
                    return "false";
            }
            return null;
        }

        /// <summary>
        /// Valueconverter for converting a string back to bool
        /// </summary>
        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            //throw new NotImplementedException();
            switch (value)
            {
                case false:
                    return "1";
                case true:
                    return "0";
                case "true":
                    return "0";
                case "false":
                    return "1";
            }
            return null;
        }
    }
}
