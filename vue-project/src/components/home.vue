<template>
  <div>
    <h1>Welcome to the Employee Management System</h1>
    <div class="nav-links">
      <router-link to="/department" class="nav-link">Manage Departments</router-link>
      <router-link to="/employee" class="nav-link">Manage Employees</router-link>
      <router-link to="/employee-report" class="nav-link">View Employee Report</router-link>
    </div>
  </div>
</template>

<style scoped>
div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  padding: 20px;
}

h1 {
  font-family: 'Poppins', sans-serif;
  font-size: 2.5rem;
  color: #1e3a8a;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  animation: fadeIn 1s ease-in-out;
  margin-bottom: 2rem;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.nav-link {
  display: inline-block;
  padding: 12px 24px;
  background-color: #3b82f6;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-family: 'Poppins', sans-serif;
  font-size: 1.2rem;
  transition: background-color 0.3s, transform 0.2s;
}

.nav-link:hover {
  background-color: #2563eb;
  transform: translateY(-2px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 600px) {
  h1 {
    font-size: 1.8rem;
  }

  .nav-link {
    font-size: 1rem;
    padding: 10px 20px;
  }
}
</style>