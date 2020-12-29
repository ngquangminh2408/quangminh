using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AppLibarary
{
    public partial class frmOverview : Form
    {
        dbLibraryDataContext db = new dbLibraryDataContext();
        public frmOverview()
        {
            InitializeComponent();
        }

        private void frmOverview_Load(object sender, EventArgs e)
        {
            loadtoTreeView(db.BookShelfs.ToList<BookShelf>());
            ListViewconfig();
        }
        public void loadtoTreeView(IEnumerable<BookShelf> myList)
        {
            Treelib.Nodes.Clear();
            TreeNode nGoc = new TreeNode("Library");
            nGoc.Tag = "";
            this.Treelib.Nodes.Add(nGoc);
            clsMynode mn;
            foreach (var o in myList)
            {
                mn = new clsMynode("BookSelft " + o.bookShelfID);
                mn.MyBookShelftID = o.bookShelfID;
                mn.Tag = o.bookShelfID;
                this.Treelib.Nodes[0].Nodes.Add(mn);
            }
            Treelib.ExpandAll();
        }
        public IEnumerable<Book> getBook(string id)
        {
            IEnumerable<Book> b;
            if (id.Equals(""))
            {
                b = db.Books.Select(t => t);
            }
            else
                b = db.Books.Where(t => t.bookShelfID.Equals(id)).Select(t => t);
            return b;

        }
        private void loadTreeViewtoListView(ListView lvw, IEnumerable<Book> book) //IEnumerable la kieu du lieu
        {
            lvw.Items.Clear();
            ListViewItem lvwitem;
            foreach (Book b in book)
            {
                lvwitem = new ListViewItem();
                lvwitem.Text = b.bookID;
                lvwitem.SubItems.Add(b.bookName);
                lvwitem.SubItems.Add(b.kind);
                lvwitem.SubItems.Add(b.publisherID);
                lvwitem.SubItems.Add(b.bookShelfID);
                lvwitem.SubItems.Add(b.timeInput.ToString());
                lvwitem.SubItems.Add(b.fettle);
                lvw.Tag = b;
                lvw.Items.Add(lvwitem);

            }
            if (lvw.Items.Count != 0)
            {
                listlib.Items[0].Selected = true;
            }
        }
            private void ListViewconfig()
            {
                this.listlib.View = View.Details;
                this.listlib.FullRowSelect = true;
                this.listlib.Columns.Add("BookID", 100);
                this.listlib.Columns.Add("BookName", 100);
                this.listlib.Columns.Add("Kind", 100);
                this.listlib.Columns.Add("PublisherID", 100);
                this.listlib.Columns.Add("BookSelftID", 100);
                this.listlib.Columns.Add("Timeinput", 100);
                this.listlib.Columns.Add("Status", 100);
            }

        private void Treelib_AfterSelect(object sender, TreeViewEventArgs e)
        {
            string tn = this.Treelib.SelectedNode.Tag.ToString();
            IEnumerable<Book> b = getBook(tn);
            loadTreeViewtoListView(listlib, b);
        }

        private void listlib_SelectedIndexChanged(object sender, EventArgs e)
        {
            Book b = null;
            if (this.listlib.SelectedItems.Count > 0)
            {
                ListViewItem lvi = this.listlib.SelectedItems[0];
                this.txtBookID.Text = lvi.SubItems[0].Text;
                this.txtBookName.Text = lvi.SubItems[1].Text;
                this.txtKind.Text = lvi.SubItems[2].Text;
                this.txtPub.Text = lvi.SubItems[3].Text;
                this.txtBS.Text = lvi.SubItems[4].Text;
                this.txtTime.Text = lvi.SubItems[5].Text;
                this.txtStatus.Text = lvi.SubItems[6].Text;
            }
        }

        private void managerBookToolStripMenuItem_Click(object sender, EventArgs e)
        {
            frmManage fmn = new frmManage();
            fmn.Show();
        }
    }

}

