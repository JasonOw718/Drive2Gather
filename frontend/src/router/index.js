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
import AdminLogin from '../components/pages/admin/AdminLogin.vue'
import DriverRegistrationList from '../components/pages/admin/component/DriverRegistrationList.vue'
import DriverManagement from '../components/pages/admin/component/DriverManagement.vue'
import DriverDetails from '../components/pages/admin/component/DriverDetails.vue'
import ReportList from '../components/pages/admin/component/ReportList.vue'
import ReportDetails from '../components/pages/admin/component/ReportDetails.vue'
import AccountManagement from '../components/pages/admin/component/AccountManagement.vue'
// import AdminSettings from '../components/pages/admin/component/settings.vue'
// Placeholder for RideComplete

import { useUserStore } from '../stores/user'
import { useAdminAuthStore } from '../stores/adminAuth'
import { useDonorAuthStore } from '../stores/donorAuth'

// Import donor components
import DonorDonation from '../components/pages/donor/DonorDonation.vue'
import DonorDonationComplete from '../components/pages/donor/DonorDonationComplete.vue'
import DonorDashboard from '../components/pages/donor/DonorDashboard.vue'
import DonorHistory from '../components/pages/donor/DonorHistory.vue'
import DonorLayout from '../components/pages/donor/DonorLayout.vue'
import DonorProfile from '../components/pages/donor/DonorProfile.vue'

// Get the base URL from Vite environment
const base = import.meta.env.BASE_URL || '/Ride2Gather/';

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
      driverId: route.query.driverId,
      rideId: route.query.rideId  // Add rideId to props
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
    component: Report_Psg,
    props: route => ({
      rideId: route.query.rideId,
      driverName: route.query.driverName,
      carPlate: route.query.carPlate,
      driverCarType: route.query.driverCarType
    })
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
    path: '/portal/login',
    name: 'AdminLogin',
    component: AdminLogin
  },
  {
    path: '/portal/admin',
    component: AdminLayout,
    redirect: '/portal/admin/account-management',
    meta: { requiresAdminAuth: true },
    children: [
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
      {
        path: 'account-management',
        name: 'Account_Management',
        component: AccountManagement
      },
      {
        path: 'account-detail/:id',
        name: 'Account_Details',
        component: () => import('../components/pages/admin/component/AccountDetails.vue')
      }
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
  // Donor routes
  {
    path: '/portal/donor',
    component: DonorLayout,
    redirect: '/portal/donor/dashboard',
    meta: { requiresDonorAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'DonorDashboard',
        component: DonorDashboard,
      },
      {
        path: 'donate',
        name: 'DonorDonation',
        component: DonorDonation,
      },
      {
        path: 'donation-complete',
        name: 'DonorDonationComplete',
        component: DonorDonationComplete,
      },
      {
        path: 'history',
        name: 'DonorHistory',
        component: DonorHistory,
      },
      {
        path: 'profile',
        name: 'DonorProfile',
        component: DonorProfile,
      }
    ]
  },
  // Legacy route redirects
  {
    path: '/admin/login',
    redirect: '/portal/login'
  },
  {
    path: '/admin/:pathMatch(.*)*',
    redirect: to => `/portal/admin/${to.params.pathMatch}`
  },
  {
    path: '/donor/:pathMatch(.*)*',
    redirect: to => `/portal/donor/${to.params.pathMatch}`
  },
  // 404 route - catch all for GitHub Pages SPA routing
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(base),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  }
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const adminAuthStore = useAdminAuthStore()
  const donorAuthStore = useDonorAuthStore()
  const isAuthenticated = userStore.isAuthenticated
  const isAdminAuthenticated = adminAuthStore.isAdminAuthenticated
  const isDonorAuthenticated = donorAuthStore.isDonorAuthenticated
  
  // Initialize auth on first load
  if (from.name === undefined) {
    userStore.initializeAuth();
    adminAuthStore.initializeAdminAuth();
    donorAuthStore.initializeDonorAuth();
  }
  
  // Handle donor routes
  if (to.path.startsWith('/portal/donor')) {
    if (to.matched.some(record => record.meta.requiresDonorAuth)) {
      if (!isDonorAuthenticated) {
        next({ name: 'AdminLogin', query: { redirectFrom: 'donor' } });
        return;
      }
    }
  }
  
  // Handle admin routes
  if (to.path.startsWith('/portal/admin')) {
    // Admin login page is public
    if (to.name === 'AdminLogin') {
      // If already authenticated as admin, redirect to admin dashboard
      if (isAdminAuthenticated) {
        next({ path: '/portal/admin/account-management' });
      } else {
        next();
      }
      return;
    }
    
    // Check if admin authentication is required
    if (to.matched.some(record => record.meta.requiresAdminAuth)) {
      if (!isAdminAuthenticated) {
        next({ name: 'AdminLogin', query: { redirectFrom: 'admin' } });
        return;
      }
    }
  }
  
  // Handle regular user routes
  // Check if route requires authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'LoginRegister', query: { redirect: to.fullPath } });
    return;
  }
  
  // These routes don't require authentication
  const publicRoutes = ['Login', 'LoginRegister', 'RegisterP', 'RegisterD', 'ForgotPassword', 'AdminLogin']
  
  if (!isAuthenticated && !to.path.startsWith('/portal') && !publicRoutes.includes(to.name) && !to.meta.requiresAuth) {
    // Redirect to login if trying to access a protected route while not authenticated
    next({ name: 'LoginRegister', query: { redirect: to.fullPath } });
  } else {
    next()
  }
})

export default router
