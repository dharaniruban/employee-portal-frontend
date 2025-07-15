<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 to-gray-100 flex items-center justify-center py-6 px-4 sm:px-6 lg:px-8">
    <div class="max-w-lg w-full bg-white rounded-2xl shadow-xl p-8 transform transition-all duration-500 hover:shadow-2xl">
      <h2 class="text-3xl font-bold text-indigo-900 mb-8 text-center tracking-tight">Employee Details</h2>
      <router-link to="/employee"
                   class="w-full mb-6 bg-indigo-600 text-white py-3 px-4 rounded-lg hover:bg-indigo-700 transition duration-300 ease-in-out transform hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-indigo-500 inline-block text-center">
        Back to Employees
      </router-link>
      <div v-if="employee" class="space-y-6 animate-fade-in">
        <div class="flex justify-center">
          <div class="relative w-24 h-24 sm:w-28 sm:h-28 overflow-hidden">
            <img v-if="employee.PhotoFileName && employee.PhotoFileName !== 'default.png'"
                 :src="'http://127.0.0.1:8000/Photos/' + employee.PhotoFileName"
                 alt="Employee Photo"
                 class="w-full h-full object-contain rounded-full border-4 border-indigo-200 shadow-md">
            <div v-else class="w-full h-full flex items-center justify-center bg-gray-100 rounded-full border-4 border-indigo-200">
              <span class="text-gray-500 text-sm font-medium">No Photo</span>
            </div>
          </div>
        </div>
        <div class="flex justify-center space-x-4">
          <label for="photoUpload" 
                 class="bg-indigo-600 text-white py-3 px-4 rounded-lg hover:bg-indigo-700 transition duration-300 ease-in-out transform hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer">
            Add Photo
          </label>
          <input id="photoUpload" type="file" @change="handlePhotoUpload" accept="image/jpeg,image/png,image/gif" class="hidden" ref="photoInput" />
          <button v-if="employee.PhotoFileName !== 'default.png'" @click="removePhoto"
                  class="bg-indigo-600 text-white py-3 px-4 rounded-lg hover:bg-indigo-700 transition duration-300 ease-in-out transform hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-indigo-500">
            Remove Photo
          </button>
        </div>
        <div class="space-y-4 text-gray-700">
          <p class="text-lg"><strong class="text-indigo-800 font-semibold">ID:</strong> {{ employee.EmployeeId }}</p>
          <p class="text-lg"><strong class="text-indigo-800 font-semibold">Name:</strong> {{ employee.EmployeeName }}</p>
          <p class="text-lg"><strong class="text-indigo-800 font-semibold">Email:</strong> {{ employee.Email || 'N/A' }}</p>
          <p class="text-lg"><strong class="text-indigo-800 font-semibold">Department:</strong> {{ employee.DepartmentName }}</p>
          <p class="text-lg"><strong class="text-indigo-800 font-semibold">Date of Joining:</strong> {{ employee.DateOfJoining }}</p>
        </div>
        <div class="flex justify-center mt-6">
          <button @click="softDeleteEmployee(employee.EmployeeId)"
                  class="bg-red-500 text-white py-3 px-4 rounded-lg hover:bg-red-600 transition duration-300 ease-in-out transform hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-red-500">
            Delete Employee
          </button>
        </div>
      </div>
      <div v-else class="text-center text-gray-500 animate-pulse text-lg">Loading...</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

axios.defaults.withCredentials = true;

export default {
  data() {
    return {
      employee: null,
    };
  },
  methods: {
    async fetchEmployee() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/employee/${this.$route.params.id}/`, { withCredentials: true });
        this.employee = response.data;
      } catch (err) {
        console.error('Fetch employee error:', err);
        alert('Failed to fetch employee details.');
      }
    },
    async handlePhotoUpload(event) {
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
        const newPhotoFileName = response.data.file_name;
        await this.updateEmployeePhoto(newPhotoFileName);
        this.$refs.photoInput.value = '';
      } catch (err) {
        console.error('File upload error:', err.response?.data || err.message);
        alert('Failed to upload photo: ' + this.formatError(err.response?.data));
      }
    },
    async updateEmployeePhoto(photoFileName) {
      try {
        const payload = {
          EmployeeName: this.employee.EmployeeName,
          Email: this.employee.Email || null,
          Department: this.employee.Department,
          DateOfJoining: this.employee.DateOfJoining,
          PhotoFileName: photoFileName,
        };
        await axios.put(`http://127.0.0.1:8000/employee/${this.employee.EmployeeId}/`, payload, {
          headers: { 'X-CSRFToken': this.getCookie('csrftoken') },
          withCredentials: true,
        });
        this.employee.PhotoFileName = photoFileName;
        alert('Photo updated successfully!');
      } catch (err) {
        console.error('Update employee photo error:', err.response?.data);
        alert('Failed to update photo: ' + this.formatError(err.response?.data));
      }
    },
    async removePhoto() {
      try {
        const payload = {
          EmployeeName: this.employee.EmployeeName,
          Email: this.employee.Email || null,
          Department: this.employee.Department,
          DateOfJoining: this.employee.DateOfJoining,
          PhotoFileName: 'default.png',
        };
        await axios.put(`http://127.0.0.1:8000/employee/${this.employee.EmployeeId}/`, payload, {
          headers: { 'X-CSRFToken': this.getCookie('csrftoken') },
          withCredentials: true,
        });
        this.employee.PhotoFileName = 'default.png';
        alert('Photo removed successfully!');
      } catch (err) {
        console.error('Remove photo error:', err.response?.data);
        alert('Failed to remove photo: ' + this.formatError(err.response?.data));
      }
    },
    async softDeleteEmployee(id) {
      try {
        await axios.patch(`http://127.0.0.1:8000/employee/${id}/`, { is_active: false }, {
          headers: { 'X-CSRFToken': this.getCookie('csrftoken') },
          withCredentials: true,
        });
        this.$router.push('/employee');
        alert('Employee soft deleted successfully!');
      } catch (err) {
        console.error('PATCH error:', err.response?.data);
        alert('Failed to soft delete employee: ' + this.formatError(err.response?.data));
      }
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
  mounted() {
    this.fetchEmployee();
  },
};
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

img {
  max-width: 400px;
  max-height: 400px;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

.hidden {
  display: none;
}
</style>