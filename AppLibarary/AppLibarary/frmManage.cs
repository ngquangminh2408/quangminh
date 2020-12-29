using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AppLibarary
{
    public partial class frmManage : Form
    {
        dbLibraryDataContext db = new dbLibraryDataContext();
        public frmManage()
        {
            InitializeComponent();
            
        }

        private void frmManage_Load(object sender, EventArgs e)
        {
            
            loaddata();
            Lock() ;
            addDataToCombobox(db.BookShelfs.ToList<BookShelf>());
            frmOverview frmo = new frmOverview();
            frmo.Close();
        }
        public void loaddata()
        {
            IEnumerable<Book> Mylist = db.Books.ToList<Book>();
            loaddatatoGridView(Mylist);
        }
        public void loaddatatoGridView(IEnumerable<Book> mylist)
        {
            this.dataGridView1.ClearSelection();
            BindingSource b = new BindingSource();
            b.DataSource = mylist;
            this.dataGridView1.DataSource = b;
            this.bindingNavigator1.BindingSource = b;
            this.dataGridView1.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            this.dataGridView1.Columns[0].HeaderText = "BookID";
            this.dataGridView1.Columns[1].HeaderText = "BookName";
            this.dataGridView1.Columns[2].HeaderText = "Kind";
            this.dataGridView1.Columns[3].HeaderText = "PublisherID";
            this.dataGridView1.Columns[4].HeaderText = "BookShelfID";
            this.dataGridView1.Columns[5].HeaderText = "timeInput";
            this.dataGridView1.Columns[6].HeaderText = "Status";
        }

        private void dataGridView1_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            if (dataGridView1.SelectedCells.Count > 0)
            {
                txtBookID.Text = dataGridView1.SelectedCells[0].Value.ToString();
                txtBookName.Text = dataGridView1.SelectedCells[1].Value.ToString();
                txtKind.Text = dataGridView1.SelectedCells[2].Value.ToString();
                txtPub.Text = dataGridView1.SelectedCells[3].Value.ToString();
                txtBS.Text = dataGridView1.SelectedCells[4].Value.ToString();
                txtTime.Text = dataGridView1.SelectedCells[5].Value.ToString();
                txtStatus.Text = Convert.ToString(dataGridView1.SelectedCells[6].Value);
            }
            else
            {
                MessageBox.Show("!!!!!!!!!");
            }
        }
        public void UnLock()
        {
            txtBookID.ReadOnly = false;
            txtBookName.ReadOnly = false;
            txtKind.ReadOnly = false;
            txtPub.ReadOnly = false;
            txtBS.ReadOnly = false;
            txtTime.ReadOnly = false;
            txtStatus.ReadOnly = false;
            btnCancel.Enabled = true;
        }

        public void Lock()
        {
            txtBookID.ReadOnly = true;
            txtBookName.ReadOnly = true;
            txtKind.ReadOnly = true;
            txtPub.ReadOnly = true;
            txtBS.ReadOnly = true;
            txtTime.ReadOnly = true;
            txtStatus.ReadOnly = true;
            btnCancel.Enabled = false;

        }
        public bool checkBookID()
        {
            IEnumerable<Book> mylist = db.Books.ToList<Book>();
            foreach (var o in mylist)
            {
                if (txtBookID.Text.Equals(o.bookID))
                {
                    return true;
                }
            }
            return false;
        }

        public bool checkBookShelfID()
        {
            IEnumerable<BookShelf> mylist = db.BookShelfs.ToList<BookShelf>();
            foreach (var o in mylist)
            {
                if (txtBS.Text.Equals(o.bookShelfID))
                {
                    return true;
                }
            }
            return false;
        }
        public void ClearTextbox()
        {
            txtBookID.Text = "";
            txtBookName.Text = "";
            txtKind.Text = "";
            txtPub.Text = "";
            txtBS.Text = "";
            txtTime.Text = "";
            txtStatus.Text = "";
        }
        private void btnAdd_Click(object sender, EventArgs e)
        {
            if (btnAdd.Text.Equals("ADDBOOK"))
            {
                btnAdd.Text = "Adding";
                btnSave.Enabled = true;
                btnAdd.Enabled = false;
                btnUpdate.Enabled = false;
                dataGridView1.Enabled = false;
                UnLock();
                bindingNavigatorDeleteItem.Enabled = false;
            }
        }

        private void bindingNavigatorDeleteItem_Click(object sender, EventArgs e)
        {
            if (dataGridView1.SelectedCells.Count > 0 && txtBookID.Text != "")
            {
                Book b = new Book();
                b = db.Books.Where(s => s.bookID == txtBookID.Text).Single();
                db.Books.DeleteOnSubmit(b);
                db.SubmitChanges();
                btnUpdate.Enabled = true;
                ClearTextbox();
                MessageBox.Show("Delete complete", "Announcement", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
                loaddata();
            }
            else
            {
                MessageBox.Show("Please choose book to delete !", "Announcement", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void btnSave_Click(object sender, EventArgs e)
        {

            //Saving of Addtion
            if (btnAdd.Text.Equals("Adding"))
            {
                if (checkBookID())
                {
                    MessageBox.Show("Identical Code BookID", "Announcement");
                    return;
                }
                if (!checkBookShelfID())
                {
                    MessageBox.Show("BookShelfID isn't available", "Announcement");
                    return;
                }
                Book b = new Book();
                b.bookID = txtBookID.Text;
                b.bookName = txtBookName.Text;
                b.bookShelfID = txtBS.Text;
                b.kind = txtKind.Text;
                b.publisherID = txtPub.Text;
                b.fettle = txtStatus.Text;
                b.timeInput = Convert.ToDateTime(txtTime.Text);
                db.Books.InsertOnSubmit(b);
                db.SubmitChanges();

                MessageBox.Show("Add complete", "Announcement", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
                btnAdd.Text = "Add";
                btnAdd.Enabled = true;
                btnSave.Enabled = false;
                dataGridView1.Enabled = true;
                ClearTextbox();
                Lock();
                loaddata();
            }
            //Saving of update
            else if (btnUpdate.Text.Equals("Updating"))
            {
                Book b = new Book();
                b = db.Books.Where(t => t.bookID == txtBookID.Text).Single();
                if (txtBookName.Text != "")
                {
                    b.bookName = txtBookName.Text;
                }
                if (txtTime.Text != "")
                {
                    b.timeInput = Convert.ToDateTime(txtTime.Text);
                }
                if (txtPub.Text != "")
                {
                    b.publisherID = txtPub.Text;
                }
                if (txtStatus.Text != "")
                {
                    b.fettle = txtStatus.Text;
                }
                
                db.SubmitChanges();
                MessageBox.Show("Update complete");
                btnUpdate.Text = "Update";
                btnAdd.Enabled = true;
                btnSave.Enabled = false;
                dataGridView1.Enabled = true;
                bindingNavigatorDeleteItem.Enabled = true;
                ClearTextbox();
                Lock();
            }
        }

        private void btnUpdate_Click(object sender, EventArgs e)
        {
            if (btnUpdate.Text.Equals("UPDATE"))
            {
                btnUpdate.Text = "Updating";
                btnSave.Enabled = true;
                btnCancel.Enabled = true;
                btnAdd.Enabled = false;
                btnUpdate.Enabled = false;
                Lock();
                txtBookName.ReadOnly = false;
                txtTime.ReadOnly = false;
                txtStatus.ReadOnly = false;
                txtPub.ReadOnly = false;
                dataGridView1.Enabled = false;
                bindingNavigatorDeleteItem.Enabled = false;
            }
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            if (btnAdd.Text.Equals("Adding"))
            {
                btnAdd.Text = "Add";
                Lock();
                btnSave.Enabled = false;
                btnCancel.Enabled = false;
                btnAdd.Enabled = true;
                btnUpdate.Enabled = true;
                dataGridView1.Enabled = true;
                bindingNavigatorDeleteItem.Enabled = true;
                ClearTextbox();
            }
            else if (btnUpdate.Text.Equals("Updating"))
            {
                btnUpdate.Text = "Update";
                Lock();
                btnSave.Enabled = false;
                btnCancel.Enabled = false;
                btnAdd.Enabled = true;
                btnUpdate.Enabled = false;
                dataGridView1.Enabled = true;
                bindingNavigatorDeleteItem.Enabled = true;
                ClearTextbox();
            }
        }
        //Bieu Thuc Chinh Qui
        private bool check(string s)
        {
            Regex rg = new Regex(@"^[A-Z]\w+");
            return rg.IsMatch(s);
        }

        private void BookName_Leave(object sender, EventArgs e)
        {
            if (this.txtBookName.Text != "")
            {
                if (check(this.txtBookName.Text))
                    this.lbBookName.Text = "*";
                else
                    this.lbBookName.Text = "Wrong";
            }
            else
                this.lbBookName.Text = "Empty";
        }
        private bool checkDate(string s)
        {
            Regex rg = new Regex(@"^\d{4}/\d{2}/\d{2}$");
            return rg.IsMatch(s);
        }

        private void txtPub_Leave(object sender, EventArgs e)
        {
            if (this.txtPub.Text != "")
            {
                if (check(this.txtPub.Text))
                    this.lbPubID.Text = "*";
                else
                    this.lbPubID.Text = "Wrong";
            }
            else
                this.lbPubID.Text = "Empty";
        }
       

        private void txtTime_leave(object sender, EventArgs e)
        {
            if (this.txtTime.Text != "")
            {
                if (checkDate(this.txtTime.Text))
                    this.lbTime.Text = "*";
                else
                    this.lbTime.Text = "Wrong (yyyy/mm/dd)";
            }
            else
                this.lbTime.Text = "Empty";
        }

        private void btnFind_Click(object sender, EventArgs e)
        {
            try
            {
                //  Block of code to try
                Book b = new Book();
                b = db.Books.Where(s => s.bookID == txtSearch.Text).Single();
                this.txtBookID.Text = b.bookID;
                this.txtBookName.Text = b.bookName;
                this.txtKind.Text = b.kind;
                this.txtPub.Text = b.publisherID;
                this.txtBS.Text = b.BookShelf.ToString();
                this.txtTime.Text = b.timeInput.ToString();
                this.txtStatus.Text = b.fettle;
            }
            catch (Exception ex)
            {
                //  Block of code to handle errors
                //MessageBox.Show(e);
                Console.Write(ex);
            }
        }
        private void addDataToCombobox(IEnumerable<BookShelf> myList)
        {
            
            foreach(var o in myList)
            {
                this.comboBox1.Items.Add(o.bookShelfID);
                
            }

        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            
            var o = comboBox1.SelectedItem;
            IEnumerable<Book> b ;
            b = db.Books.Where(t => t.bookShelfID == comboBox1.SelectedItem);
            loaddatatoGridView(b);
        }

        private void comBoBox_leave(object sender, EventArgs e)
        {
            
            
        }

        private void btnShow_Click(object sender, EventArgs e)
        {
            IEnumerable<Book> Mylist = db.Books.ToList<Book>();
            loaddatatoGridView(Mylist);
        }
    }
}
