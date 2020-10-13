using Dragablz;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SomUI.ViewModel
{
    /// <summary>
    /// ViewModel for managing dragged tabs.
    /// </summary>
    public class TabViewModel
    {
        private readonly IInterTabClient _interTabClient;

        /// <summary>
        /// Create InterTabClient
        /// </summary>
        public TabViewModel()
        {
            _interTabClient = new MyInterTabClient();
        }
        /// <summary>
        /// Get InterTabClient
        /// </summary>
        /// <returns>Returns InterTabClient.</returns>
        public IInterTabClient InterTabClient
        {
            get { return _interTabClient; }
        }
    }
}
