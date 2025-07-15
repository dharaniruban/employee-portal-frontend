<template>
  <div>
    <h2>Department Management</h2>
    <input v-model="searchTerm" placeholder="Search by ID or Name" />
    <form @submit.prevent="isEdit ? updateDepartment() : addDepartment()" class="form">
      <input v-model="form.DepartmentName" placeholder="Department Name" required />
      <button type="submit">{{ isEdit ? "Update" : "Add" }} Department</button>
      <button type="button" @click="resetForm()" v-if="isEdit">Cancel</button>
    </form>
    <div v-if="loading">Loading...</div>
    <table v-else border="1" cellpadding="8" cellspacing="0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Department Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="dept in filteredDepartments" :key="dept.DepartmentId">
          <td>{{ dept.DepartmentId }}</td>
          <td>{{ dept.DepartmentName }}</td>
          <td>
            <button @click="editDepartment(dept)">Edit</button>
            <button @click="softDeleteDepartment(dept.DepartmentId)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="departments.length && !loading">
      <button @click="fetchDepartments(currentPage - 1)" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="fetchDepartments(currentPage + 1)" :disabled="currentPage === totalPages">Next</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      departments: [],
      form: {
        DepartmentName: '',
      },
      isEdit: false,
      editId: null,
      searchTerm: '',
      loading: false,
      currentPage: 1,
      totalPages: 1,
    };
  },
  computed: {
    filteredDepartments() {
      const term = this.searchTerm.toLowerCase();
      return this.departments.filter(
        d =>
          d.DepartmentName.toLowerCase().includes(term) ||
          String(d.DepartmentId).includes(term)
      );
    },
  },
  methods: {
    async fetchDepartments(page = 1) {
      this.loading = true;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/department/?page=${page}`);
        this.departments = response.data.results || response.data;
        this.currentPage = page;
        this.totalPages = Math.ceil(response.data.count / 10) || 1;
      } catch (err) {
        console.error('Fetch departments error:', err);
        alert('Failed to fetch departments.');
      } finally {
        this.loading = false;
      }
    },
    async addDepartment() {
      this.loading = true;
      try {
        await axios.post('http://127.0.0.1:8000/department/', this.form, {
          headers: { 'X-CSRFToken': this.getCookie('csrftoken') },
        });
        this.fetchDepartments();
        this.resetForm();
        alert('Department added successfully!');
      } catch (err) {
        console.error('POST error:', err.response?.data);
        alert('Failed to add department: ' + this.formatError(err.response?.data));
      } finally {
        this.loading = false;
      }
    },
    editDepartment(dept) {
      this.isEdit = true;
      this.editId = dept.DepartmentId;
      this.form = { DepartmentName: dept.DepartmentName };
    },
    async updateDepartment() {
      this.loading = true;
      try {
        await axios.put(`http://127.0.0.1:8000/department/${this.editId}/`, this.form, {
          headers: { 'X-CSRFToken': this.getCookie('csrftoken') },
        });
        this.fetchDepartments();
        this.resetForm();
        alert('Department updated successfully!');
      } catch (err) {
        console.error('PUT error:', err.response?.data);
        alert('Failed to update department: ' + this.formatError(err.response?.data));
      } finally {
        this.loading = false;
      }
    },
    async softDeleteDepartment(id) {
      this.loading = true;
      try {
        await axios.patch(`http://127.0.0.1:8000/department/${id}/`, { is_active: false }, {
          headers: { 'X-CSRFToken': this.getCookie('csrftoken') },
        });
        this.fetchDepartments();
        alert('Department soft deleted successfully!');
      } catch (err) {
        console.error('PATCH error:', err.response?.data);
        alert('Failed to soft delete department: ' + this.formatError(err.response?.data));
      } finally {
        this.loading = false;
      }
    },
    resetForm() {
      this.form = { DepartmentName: '' };
      this.isEdit = false;
      this.editId = null;
    },
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + '=') {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },
    formatError(error) {
      if (!error) return 'Unknown error';
      if (typeof error === 'string') return error;
      if (error.detail) return error.detail;
      return Object.values(error).flat().join(', ');
    },
  },
  mounted() {
    this.fetchDepartments();
  },
};
</script>

<style scoped>
div {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Poppins', sans-serif;
}

h2 {
  color: #1e3a8a;
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.8rem;
}

input[type="text"] {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input[type="text"]:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
}

.form {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.form input {
  flex: 1;
  min-width: 150px;
  padding: 10px;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form input:focus {
  outline: none;
  border-color: #3b82f6;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.form button[type="submit"] {
  background: #3b82f6;
  color: white;
}

.form button[type="submit"]:hover {
  background: #2563eb;
  transform: translateY(-2px);
}

.form button[type="button"] {
  background: #ef4444;
  color: white;
}

.form button[type="button"]:hover {
  background: #dc2626;
  transform: translateY(-2px);
}

table button:nth-child(1) {
  background: #10b981;
  color: white;
  margin-right: 5px;
}

table button:nth-child(1):hover {
  background: #059669;
  transform: translateY(-2px);
}

table button:nth-child(2) {
  background: #ef4444;
  color: white;
}

table button:nth-child(2):hover {
  background: #dc2626;
  transform: translateY(-2px);
}

table {
  width: 100%;
  border-collapse: collapse;
  background: #f9fafb;
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  padding: 12px;
  text-align: left;
}

th {
  background: #3b82f6;
  color: white;
  font-weight: 600;
}

tbody tr {
  border-bottom: 1px solid #e5e7eb;
}

tbody tr:hover {
  background: #eff6ff;
}

@media (max-width: 600px) {
  .form {
    flex-direction: column;
  }

  table {
    font-size: 0.9rem;
  }

  th, td {
    padding: 8px;
  }
}
</style>