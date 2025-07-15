<template>
  <div>
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/employee">Employee</router-link> |
      <router-link to="/department">Department</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
nav {
  padding: 10px;
  background: #f0f0f0;
}
nav a {
  margin-right: 10px;
}
</style>
