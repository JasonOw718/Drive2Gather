import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/pages/HomePage.vue'
import LoginRegister from '../components/pages/passanger/LoginRegister.vue'
import Login from '../components/pages/passanger/Login.vue'
import ForgotPassword from '../components/pages/passanger/ForgotPassword.vue'
import RegisterP from '../components/pages/passanger/RegisterP.vue'
import RegisterD from '../components/pages/driver/RegisterD.vue'
import RightNavbar from '../components/pages/rightnavbar.vue'
import ProfileP from '../components/pages/passanger/ProfileP.vue'
import ProfileD from '../components/pages/driver/ProfileD.vue'
import ChangePassword from '../components/pages/passanger/ChangePassword.vue'
import FindRide from '../components/pages/passanger/FindRide.vue'
import CreateRide from '../components/pages/driver/CreateRide.vue'
import RideList from '../components/pages/passanger/RideList.vue'
import RideDetail from '../components/pages/passanger/RideDetail.vue'
import RideDetailD from '../components/pages/driver/RideDetailD.vue'
import Ridebooked from '../components/pages/passanger/Ridebooked.vue'
import Otwpage from '../components/pages/passanger/Otwpage.vue'
import Dropoff from '../components/pages/driver/Dropoff.vue'
import Report_Psg from '../components/pages/passanger/Report_Psg.vue'
import RidecompleteD from '../components/pages/driver/RidecompleteD.vue'
import Report_D_side from '../components/pages/driver/Report_D_side.vue'
import RidecompleteP from '../components/pages/passanger/RidecompleteP.vue'
import Donation from '../components/pages/passanger/Donation.vue'
import DonateComplete from '../components/pages/passanger/donatecomplete.vue'
import ChatRoom from '../components/pages/shared/ChatRoom.vue'
import RideFilter from '../components/pages/RideFilter.vue'

import AdminLayout from '../components/pages/admin/AdminLayout.vue'
import DriverRegistrationList from '../components/pages/admin/component/DriverRegistrationList.vue'
import DriverManagement from '../components/pages/admin/component/DriverManagement.vue'
import DriverDetails from '../components/pages/admin/component/DriverDetails.vue'
import ReportList from '../components/pages/admin/component/ReportList.vue'
import ReportDetails from '../components/pages/admin/component/ReportDetails.vue'
// import AdminSettings from '../components/pages/admin/component/settings.vue'
// Placeholder for RideComplete

import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/find-ride',
    name: 'FindRide',
    component: FindRide
  },
  {
    path: '/create-ride',
    name: 'CreateRide',
    component: CreateRide
  },
  {
    path: '/ride-filter',
    name: 'RideFilter',
    component: RideFilter,
    meta: { requiresAuth: true }
  },
  {
    path: '/login-register',
    name: 'LoginRegister',
    component: LoginRegister
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword
  },
  {
    path: '/register-passenger',
    name: 'RegisterP',
    component: RegisterP
  },
  {
    path: '/register-driver',
    name: 'RegisterD',
    component: RegisterD
  },
  {
    path: '/rightnavbar',
    name: 'RightNavbar',
    component: RightNavbar
  },
  {
    path: '/profile',
    name: 'Profile',
    beforeEnter: (to, from, next) => {
      // Access Pinia store
      const userStore = useUserStore()
      const role = userStore.currentUser?.role
      if (role === 'passenger') {
        next({ name: 'ProfileP' })
      } else if (role === 'driver') {
        next({ name: 'ProfileD' })
      } else {
        next('/login-register') // fallback if not authenticated
      }
    }
  },
  {
    path: '/profile-passenger',
    name: 'ProfileP',
    component: ProfileP
  },
  {
    path: '/profile-driver',
    name: 'ProfileD',
    component: ProfileD
  },
  {
    path: '/change-password',
    name: 'ChangePassword',
    component: ChangePassword
  },
  {
    path: '/ride-list',
    name: 'RideList',
    component: RideList
  },
  {
    path: '/ride/:id',
    name: 'RideDetailView',
    beforeEnter: (to, from, next) => {
      const userStore = useUserStore()
      const role = userStore.currentUser?.role
      
      if (role === 'driver') {
        next({ 
          name: 'RideDetailDSide', 
          query: { id: to.params.id } 
        })
      } else {
        next({ 
          name: 'RideDetail', 
          params: { id: to.params.id },
          query: to.query // Pass through the query parameters
        })
      }
    }
  },
  {
    path: '/ride-detail/:id',
    name: 'RideDetail',
    component: RideDetail,
    props: true
  },
  {
    path: '/ride-detail-driverside',
    name: 'RideDetailDSide',
    component: RideDetailD,
    props: route => ({ 
      id: route.query.id 
    })
  },
  {
    path: '/ridebooked',
    name: 'Ridebooked',
    component: Ridebooked
  },
  {
    path: '/otw',
    name: 'Otwpage',
    component: Otwpage
  },
  {
    path: '/ride-complete',
    name: 'RideComplete',
    component: RidecompleteP,
    props: route => ({
      from: route.query.from,
      to: route.query.to,
      driverName: route.query.driverName,
      driverAvatar: route.query.driverAvatar,
      carPlate: route.query.carPlate,
      driverCarType: route.query.driverCarType,
      driverId: route.query.driverId
    })
  },
  {
    path: '/ride-completed',
    name: 'RideCompleted',
    component: RidecompleteD,
    props: route => ({
      from: route.query.from,
      to: route.query.to
    })
  },
  {
    path: '/dropoff',
    name: 'Dropoff',
    component: Dropoff
  },
  {
    path: '/Reportpage',
    name: 'ReportPsg',
    component: Report_Psg
  },
  {
    path: '/Reportpage-driver',
    name: 'ReportDside',
    component: Report_D_side
  },
  {
    path: '/ridecomplete-driver',
    name: 'RidecompleteD',
    component: RidecompleteD
  },
  {
    path: '/donation/:driverId',
    name: 'Donation',
    component: Donation,
    props: true
  },
  {
    path: '/donate-complete',
    name: 'DonateComplete',
    component: DonateComplete
  },
  {
    path: '/chat-room/:id',
    name: 'ChatRoom',
    component: ChatRoom,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    component: AdminLayout,
    redirect: '/admin/driver-registration',
    children: [
      {
        path: 'driver-registration',
        name: 'Driver_Registration_List',
        component: DriverRegistrationList
      },
      {
        path: 'driver-management',
        name: 'Driver_Management',
        component: DriverManagement
      },
      {
        path: 'driver-detail/:id',
        name: 'Driver_Details',
        component: DriverDetails
      },
      {
        path: 'report-list',
        name: 'Report_List',
        component: ReportList
      },
      {
        path: 'report-detail/:id',
        name: 'Report_Details',
        component: ReportDetails
      },
      
    ]
  },
  {
    path: '/home',
    redirect: '/',
    meta: { requiresAuth: true }
  },
  {
    path: '/ride-history',
    name: 'RideHistory',
    component: () => import('../components/pages/RideHistory.vue'),
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isAuthenticated = userStore.isAuthenticated
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'LoginRegister' })
    return
  }
  
  // These routes don't require authentication
  const publicRoutes = ['Login', 'LoginRegister', 'RegisterP', 'RegisterD', 'ForgotPassword']
  
  if (!isAuthenticated && !publicRoutes.includes(to.name) && !to.meta.requiresAuth) {
    // Redirect to login if trying to access a protected route while not authenticated
    next({ name: 'LoginRegister' })
  } else {
    next()
  }
})

export default router
