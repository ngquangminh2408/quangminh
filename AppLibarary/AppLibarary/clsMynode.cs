using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AppLibarary
{
    class clsMynode :System.Windows.Forms.TreeNode
    {
        private string myBookShelftID;

        public string MyBookShelftID { get => myBookShelftID; set => myBookShelftID = value; }
        public clsMynode(String s)
        {
            this.Text = s;
        }
    }
}
