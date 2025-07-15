<template>
  <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h2 class="text-3xl font-bold text-gray-800 mb-4 text-center">Employee Management</h2>
    <div class="mb-4 max-w-2xl mx-auto">
      <input v-model="searchTerm" placeholder="Search by ID, Name, or Department" 
             class="w-full p-4 text-lg border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-300" />
    </div>
    <form @submit.prevent="isEdit ? updateEmployee() : addEmployee()" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8 bg-white p-6 rounded-lg shadow-md">
      <input type="text" v-model="form.EmployeeName" placeholder="Employee Name" required 
             class="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-300" />
      <input type="email" v-model="form.Email" placeholder="Email" 
             class="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-300" />
      <select v-model="form.Department" required class="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-300">
        <option value="" disabled>Select Department</option>
        <option v-for="dept in departments" :key="dept.DepartmentId" :value="dept.DepartmentId">
          {{ dept.DepartmentName }}
        </option>
      </select>
      <input type="date" v-model="form.DateOfJoining" required 
             class="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-300" />
      <input type="file" @change="handleFileUpload" accept="image/jpeg,image/png,image/gif" ref="fileInput" :required="!isEdit" 
             class="p-3 border border-gray-300 rounded-lg" />
      <div class="flex space-x-4">
        <button type="submit" 
                class="flex-1 bg-indigo-600 text-white p-3 rounded-lg hover:bg-indigo-700 transition duration-300 transform hover:-translate-y-1">
          {{ isEdit ? "Update" : "Add" }} Employee
        </button>
        <button v-if="isEdit" type="button" @click="resetForm()" 
                class="flex-1 bg-red-500 text-white p-3 rounded-lg hover:bg-red-600 transition duration-300 transform hover:-translate-y-1">
          Cancel
        </button>
      </div>
    </form>
    <div v-if="loading" class="text-center text-gray-500 animate-pulse">Loading...</div>
    <div v-else class="overflow-x-auto bg-white rounded-lg shadow-md">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-indigo-600">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">ID</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Email</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Department</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Date Of Joining</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="emp in filteredEmployees" :key="emp.EmployeeId" class="hover:bg-indigo-50 transition duration-200">
            <td class="px-6 py-4 whitespace-nowrap">
              <router-link :to="`/employee/${emp.EmployeeId}`" class="text-indigo-600 hover:text-indigo-800">{{ emp.EmployeeId }}</router-link>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <router-link :to="`/employee/${emp.EmployeeId}`" class="text-indigo-600 hover:text-indigo-800">{{ emp.EmployeeName }}</router-link>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">{{ emp.Email || 'N/A' }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ emp.DepartmentName }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ emp.DateOfJoining }}</td>
            <td class="px-6 py-4 whitespace-nowrap space-x-2">
              <button @click="editEmployee(emp)" class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition duration-300 transform hover:-translate-y-1">Edit</button>
              <button @click="softDeleteEmployee(emp.EmployeeId)" class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition duration-300 transform hover:-translate-y-1">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="employees.length && !loading" class="flex justify-between items-center mt-6">
      <button @click="fetchEmployees(currentPage - 1)" :disabled="currentPage === 1" 
              class="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400 transition duration-300" :class="{ 'cursor-not-allowed opacity-50': currentPage === 1 }">
        Previous
      </button>
      <span class="text-gray-700">Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="fetchEmployees(currentPage + 1)" :disabled="currentPage === totalPages" 
              class="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400 transition duration-300" :class="{ 'cursor-not-allowed opacity-50': currentPage === totalPages }">
        Next
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

// Configure axios to include credentials (e.g., CSRF token in cookies)
axios.defaults.withCredentials = true;

export default {
  data() {
    return {
      employees: [],
      departments: [],
      form: {
        EmployeeName: '',
        Email: '',
        Department: '',
        DateOfJoining: '',
        PhotoFileName: 'default.png',
        file: null,
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
    filteredEmployees() {
      const term = this.searchTerm.toLowerCase();
      return this.employees.filter(
        e =>
          e.EmployeeName.toLowerCase().includes(term) ||
          (e.Email || '').toLowerCase().includes(term) ||
          e.DepartmentName.toLowerCase().includes(term) ||
          String(e.EmployeeId).includes(term)
      );
    },
  },
  methods: {
    async fetchCsrfToken() {
      try {
        await axios.get('http://127.0.0.1:8000/', { withCredentials: true });
        const token = this.getCookie('csrftoken');
        if (token) {
          console.log('CSRF token fetched:', token);
        } else {
          console.warn('CSRF token not found after fetch');
        }
      } catch (err) {
        console.error('Failed to fetch CSRF token:', err);
      }
    },
    async fetchDepartments() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/department/', { withCredentials: true });
        this.departments = response.data.results || response.data;
      } catch (err) {
        console.error('Fetch departments error:', err);
        alert('Failed to fetch departments.');
      }
    },
    async fetchEmployees(page = 1) {
      this.loading = true;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/employee/?page=${page}`, { withCredentials: true });
        this.employees = response.data.results || response.data;
        this.currentPage = page;
        this.totalPages = Math.ceil(response.data.count / 10) || 1;
      } catch (err) {
        console.error('Fetch employees error:', err);
        alert('Failed to fetch employees.');
      } finally {
        this.loading = false;
      }
    },
    async handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) {
        console.error('No file selected');
        alert('Please select a file to upload.');
        return;
      }
      console.log('Selected file:', file.name, 'Size:', file.size, 'Type:', file.type);
      const formData = new FormData();
      formData.append('file', file);
      try {
        const response = await axios.post('http://127.0.0.1:8000/savefile/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': this.getCookie('csrftoken'),
          },
          withCredentials: true,
        });
        console.log('File upload response:', response.data);
        this.form.PhotoFileName = response.data.file_name;
      } catch (err) {
        console.error('File upload error:', err.response?.data || err.message);
        alert('Failed to upload photo: ' + this.formatError(err.response?.data));
      }
    },
    async addEmployee() {
      this.loading = true;
      try {
        const payload = {
          EmployeeName: this.form.EmployeeName,
          Email: this.form.Email || null,
          Department: this.form.Department,
          DateOfJoining: this.form.DateOfJoining,
          PhotoFileName: this.form.PhotoFileName,
        };
        await axios.post('http://127.0.0.1:8000/employee/', payload, {
          headers: { 'X-CSRFToken': this.getCookie('csrftoken') },
          withCredentials: true,
        });
        this.fetchEmployees();
        this.resetForm();
        alert('Employee added successfully!');
      } catch (err) {
        console.error('POST error:', err.response?.data);
        alert('Failed to add employee: ' + this.formatError(err.response?.data));
      } finally {
        this.loading = false;
      }
    },
    editEmployee(emp) {
      this.isEdit = true;
      this.editId = emp.EmployeeId;
      this.form = {
        EmployeeName: emp.EmployeeName,
        Email: emp.Email || '',
        Department: emp.Department,
        DateOfJoining: emp.DateOfJoining,
        PhotoFileName: emp.PhotoFileName,
        file: null,
      };
    },
    async updateEmployee() {
      this.loading = true;
      try {
        const payload = {
          EmployeeName: this.form.EmployeeName,
          Email: this.form.Email || null,
          Department: this.form.Department,
          DateOfJoining: this.form.DateOfJoining,
          PhotoFileName: this.form.PhotoFileName,
        };
        await axios.put(`http://127.0.0.1:8000/employee/${this.editId}/`, payload, {
          headers: { 'X-CSRFToken': this.getCookie('csrftoken') },
          withCredentials: true,
        });
        this.fetchEmployees();
        this.resetForm();
        alert('Employee updated successfully!');
      } catch (err) {
        console.error('PUT error:', err.response?.data);
        alert('Failed to update employee: ' + this.formatError(err.response?.data));
      } finally {
        this.loading = false;
      }
    },
    async softDeleteEmployee(id) {
      this.loading = true;
      try {
        await axios.patch(`http://127.0.0.1:8000/employee/${id}/`, { is_active: false }, {
          headers: { 'X-CSRFToken': this.getCookie('csrftoken') },
          withCredentials: true,
        });
        this.fetchEmployees();
        alert('Employee soft deleted successfully!');
      } catch (err) {
        console.error('PATCH error:', err.response?.data);
        alert('Failed to soft delete employee: ' + this.formatError(err.response?.data));
      } finally {
        this.loading = false;
      }
    },
    resetForm() {
      this.form = {
        EmployeeName: '',
        Email: '',
        Department: '',
        DateOfJoining: '',
        PhotoFileName: 'default.png',
        file: null,
      };
      this.isEdit = false;
      this.editId = null;
      this.$refs.fileInput.value = '';
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
      if (!cookieValue) {
        console.warn('CSRF token not found');
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
  async mounted() {
    await this.fetchCsrfToken();
    await this.fetchDepartments();
    await this.fetchEmployees();
  },
};
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.container {
  animation: fadeIn 0.5s ease-out;
  max-width: 900px;
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

input[type="text"],
input[type="email"],
input[type="date"],
input[type="file"],
select {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input:focus,
select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
}

form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

form button[type="submit"] {
  background: #3b82f6;
  color: white;
}

form button[type="submit"]:hover {
  background: #2563eb;
  transform: translateY(-2px);
}

form button[type="button"] {
  background: #ef4444;
  color: white;
}

form button[type="button"]:hover {
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
  form {
    grid-template-columns: 1fr;
  }

  table {
    font-size: 0.9rem;
  }

  th, td {
    padding: 8px;
  }
}
</style>