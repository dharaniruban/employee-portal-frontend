import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/home.vue';
import Department from '../components/department.vue';
import Employee from '../components/employee.vue';
import EmployeeDetail from '../components/employeeDetail.vue';
import EmployeeChart from '../components/EmployeeChart.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/department', component: Department },
  { path: '/employee', component: Employee },
  { path: '/employee/:id', component: EmployeeDetail, props: true },
  { path: '/employee-report', component: EmployeeChart },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;