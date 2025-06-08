<template>
  <div class="min-h-screen pt-[max(2.5rem,env(safe-area-inset-top))] pb-[max(env(safe-area-inset-bottom),2.5rem)] px-6 bg-white flex flex-col justify-between relative" style="max-width:375px;margin:0 auto;">
    <!-- Back Button -->
    <button
      class="absolute top-4 left-4 w-10 h-10 flex items-center justify-center rounded-lg bg-[#F5F5F5] z-20 border border-gray-200"
      @click="$router.back()"
      aria-label="Back"
    >
      <span class="w-5 h-5 text-primary">
        <font-awesome-icon icon="fa-arrow-left" class="text-[#C77DFF] w-5 h-5" />
      </span>
    </button>
    <!-- Title -->
    <div class="block font-medium text-left text-[24px] text-gray-900 mt-10 mb-6">Register</div>
    
    <!-- Auth Error Message -->
    <p v-if="userStore.authError" class="text-red-500 text-sm mb-4">{{ userStore.authError }}</p>
    
    <form class="flex flex-col gap-5 flex-1" @submit.prevent="onSubmit">
      <!-- Username -->
      <div>
        <label for="username" class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Username</label>
        <input id="username" v-model="username" type="text" placeholder="Username" class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-base rounded-lg text-black" />
        <p v-if="usernameError" class="text-red-500 text-sm mt-1">{{ usernameError }}</p>
      </div>
      <!-- Email -->
      <div>
        <label for="email" class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Email</label>
        <input id="email" v-model="email" type="email" placeholder="Email" class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-base rounded-lg text-black" />
        <p v-if="emailError" class="text-red-500 text-sm mt-1">{{ emailError }}</p>
      </div>
      <!-- Phone Number -->
      <div class="relative">
        <label for="phone" class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Phone Number</label>
        <div class="absolute top-3.5 left-0 pl-4 pt-7 pointer-events-none">
          <span class="text-gray-400 text-base">+60</span>
        </div>
        <input id="phone" v-model="phone" type="tel" placeholder="Phone Number" maxlength="10" @input="onPhoneInput" class="w-full border border-gray-200 bg-[#F5F5F5] px-14 py-3 focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-base rounded-lg text-black" />
        <p v-if="phoneError" class="text-red-500 text-sm mt-1">{{ phoneError }}</p>
      </div>
      <!-- Password -->
      <div>
        <label for="password" class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Password</label>
        <div class="flex items-center w-full bg-[#F5F5F5] border border-gray-200 rounded-lg focus-within:ring-2 focus-within:ring-[#C77DFF]">
          <input
            id="password"
            :type="showPassword ? 'text' : 'password'"
            v-model="password"
            placeholder="Password"
            class="flex-1 min-w-0 bg-transparent px-4 py-3 text-base text-black focus:outline-none rounded-lg"
          />
          <button
            type="button"
            class="shrink-0 ml-[-2.5rem] mr-3 h-full flex items-center justify-center bg-transparent border-none focus:outline-none"
            @click="showPassword = !showPassword"
            tabindex="-1"
            aria-label="Toggle password visibility"
          >
            <font-awesome-icon :icon="showPassword ? 'fa-eye-slash' : 'fa-eye'" class="text-[#C77DFF] w-5 h-5" />
          </button>
        </div>
        <p v-if="passwordError" class="text-red-500 text-sm mt-1">{{ passwordError }}</p>
      </div>
      <!-- Confirm Password -->
      <div>
        <label for="confirmPassword" class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Confirm Password</label>
        <div class="flex items-center w-full bg-[#F5F5F5] border border-gray-200 rounded-lg focus-within:ring-2 focus-within:ring-[#C77DFF]">
          <input
            id="confirmPassword"
            :type="showConfirmPassword ? 'text' : 'password'"
            v-model="confirmPassword"
            placeholder="Confirm Password"
            class="flex-1 min-w-0 bg-transparent px-4 py-3 text-base text-black focus:outline-none rounded-lg"
          />
          <button
            type="button"
            class="shrink-0 ml-[-2.5rem] mr-3 h-full flex items-center justify-center bg-transparent border-none focus:outline-none"
            @click="showConfirmPassword = !showConfirmPassword"
            tabindex="-1"
            aria-label="Toggle password visibility"
          >
            <font-awesome-icon :icon="showConfirmPassword ? 'fa-eye-slash' : 'fa-eye'" class="text-[#C77DFF] w-5 h-5" />
          </button>
        </div>
        <p v-if="confirmPasswordError" class="text-red-500 text-sm mt-1">{{ confirmPasswordError }}</p>
      </div>
      <!-- License Number -->
      <div>
        <label for="licenseNumber" class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">License Number</label>
        <input id="licenseNumber" v-model="licenseNumber" type="text" placeholder="License Number" class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-base rounded-lg text-black" />
        <p v-if="licenseNumberError" class="text-red-500 text-sm mt-1">{{ licenseNumberError }}</p>
      </div>
      <!-- Car Type -->
      <div>
        <label for="carType" class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Car Type</label>
        <input id="carType" v-model="carType" type="text" placeholder="Honda CR-V" class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-base rounded-lg text-black" />
        <p v-if="carTypeError" class="text-red-500 text-sm mt-1">{{ carTypeError }}</p>
      </div>
      <!-- Car Color -->
      <div>
        <label for="carColor" class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Car Color</label>
        <input id="carColor" v-model="carColor" type="text" placeholder="White" class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-base rounded-lg text-black" />
        <p v-if="carColorError" class="text-red-500 text-sm mt-1">{{ carColorError }}</p>
      </div>
      <!-- Car Plate -->
      <div>
        <label for="carPlate" class="block text-[18px] font-semibold text-gray-800 mb-1 text-left">Car Plate</label>
        <input id="carPlate" v-model="carPlate" type="text" placeholder="VLN 0314" class="w-full border border-gray-200 bg-[#F5F5F5] px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#C77DFF] text-base rounded-lg text-black" />
        <p v-if="carPlateError" class="text-red-500 text-sm mt-1">{{ carPlateError }}</p>
      </div>
      <!-- Upload Photo Section -->
      <div class="mt-6">
        <label class="block text-[18px] font-bold text-gray-800 mb-1 text-left">Photo</label>
        <div class="text-sm text-gray-500  text-left mb-2">Selfieee</div>
        <div class="flex gap-3">
          <div v-for="(file, idx) in photoFiles" :key="'photo-'+idx" class="relative">
            <input type="file" accept="image/jpeg,image/png" class="hidden" :id="'photo-upload-'+idx" @change="e => onFileChange(e, 'photo', idx)" />
            <label :for="'photo-upload-'+idx" class="w-20 h-20 flex items-center justify-center bg-[#F5F5F5] border border-gray-300 rounded-lg cursor-pointer hover:shadow-md transition">
                <template v-if="file.preview">
                <img :src="file.preview" class="object-cover w-full h-full rounded-lg" />
                </template>
                <template v-else>
                <font-awesome-icon :icon="['fas', 'plus']" class="text-[#C77DFF] text-2xl" />
                </template>
            </label>
          </div>
        </div>
      </div>
      <div class="mt-6">
        <label class="block text-[18px] font-bold text-gray-800 mb-1 text-left">License</label>
        <div class="text-sm text-gray-500 text-left  mb-2">Capture 2 Views of Your License (Front & Back)</div>
        <div class="flex gap-3">
          <div v-for="(file, idx) in licenseFiles" :key="'license-'+idx" class="relative">
            <input type="file" accept="image/jpeg,image/png" class="hidden" :id="'license-upload-'+idx" @change="e => onFileChange(e, 'license', idx)" />
            <label :for="'license-upload-'+idx" class="w-20 h-20 flex items-center justify-center bg-[#F5F5F5] border border-gray-300 rounded-lg cursor-pointer hover:shadow-md transition">
                <template v-if="file.preview">
                <img :src="file.preview" class="object-cover w-full h-full rounded-lg" />
                </template>
                <template v-else>
                <font-awesome-icon :icon="['fas', 'plus']" class="text-[#C77DFF] text-2xl" />
                </template>
            </label>
          </div>
        </div>
      </div>
      <div class="mt-6">
        <label class="block text-[18px] font-bold text-gray-800 mb-1 text-left">Car</label>
        <div class="text-sm text-gray-500 text-left mb-2">Capture All 4 Views of Your Car</div>
        <div class="flex gap-3 overflow-x-auto whitespace-nowrap">
          <div v-for="(file, idx) in carFiles" :key="'car-'+idx" class="relative">
            <input type="file" accept="image/jpeg,image/png" class="hidden overflow-x-auto" :id="'car-upload-'+idx" @change="e => onFileChange(e, 'car', idx)" />
            <label :for="'car-upload-'+idx" class="w-20 h-20 flex items-center justify-center bg-[#F5F5F5] border border-gray-300 rounded-lg cursor-pointer hover:shadow-md transition">
                <template v-if="file.preview">
                <img :src="file.preview" class="object-cover w-full h-full rounded-lg" />
                </template>
                <template v-else>
                <font-awesome-icon :icon="['fas', 'plus']" class="text-[#C77DFF] text-2xl" />
                </template>
            </label>
          </div>
        </div>
      </div>
      <!-- Register Button -->
      <button 
        class="w-11/12 max-w-md mx-auto py-3 px-4 rounded-full shadow-md bg-[#C77DFF] text-white text-base font-bold hover:bg-opacity-90 transition-all duration-300 mt-6" 
        type="submit"
        :disabled="isLoading"
      >
        {{ isLoading ? 'Registering...' : 'Register' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '../../../stores/user'

const userStore = useUserStore()
const username = ref('')
const email = ref('')
const phone = ref('')
const password = ref('')
const confirmPassword = ref('')
const carType = ref('')
const carColor = ref('')
const carPlate = ref('')
const licenseNumber = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const usernameError = ref('')
const emailError = ref('')
const phoneError = ref('')
const passwordError = ref('')
const confirmPasswordError = ref('')
const carTypeError = ref('')
const carColorError = ref('')
const carPlateError = ref('')
const licenseNumberError = ref('')
const photoFiles = ref([{ preview: null }])
const licenseFiles = ref([{ preview: null }, { preview: null }])
const carFiles = ref([{ preview: null }, { preview: null }, { preview: null }, { preview: null }])
const isLoading = ref(false)

function validateEmail(val) {
  return /@.+\..+/.test(val)
}
function validatePhone(val) {
  return /^\d{10}$/.test(val)
}
function validatePassword(val) {
  return /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/.test(val)
}
function onPhoneInput(e) {
  phone.value = e.target.value.replace(/\D/g, '').slice(0, 10)
}
function onFileChange(e, type, idx) {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = ev => {
    if (type === 'photo') photoFiles.value[idx] = { preview: ev.target.result }
    if (type === 'license') licenseFiles.value[idx] = { preview: ev.target.result }
    if (type === 'car') carFiles.value[idx] = { preview: ev.target.result }
  }
  reader.readAsDataURL(file)
}
async function onSubmit() {
  usernameError.value = ''
  emailError.value = ''
  phoneError.value = ''
  passwordError.value = ''
  confirmPasswordError.value = ''
  carTypeError.value = ''
  carColorError.value = ''
  carPlateError.value = ''
  licenseNumberError.value = ''
  let valid = true
  
  if (!username.value) {
    usernameError.value = 'Username is required.'
    valid = false
  }
  if (!validateEmail(email.value)) {
    emailError.value = 'Please enter a valid email.'
    valid = false
  }
  if (!validatePhone(phone.value)) {
    phoneError.value = 'Enter a valid 10-digit phone number.'
    valid = false
  }
  if (!validatePassword(password.value)) {
    passwordError.value = 'Password must be at least 8 characters and include letters and numbers.'
    valid = false
  }
  if (confirmPassword.value !== password.value || !confirmPassword.value) {
    confirmPasswordError.value = 'Passwords do not match.'
    valid = false
  }
  if (!carType.value) {
    carTypeError.value = 'Car type is required.'
    valid = false
  }
  if (!carColor.value) {
    carColorError.value = 'Car color is required.'
    valid = false
  }
  if (!carPlate.value) {
    carPlateError.value = 'Car plate is required.'
    valid = false
  }
  if (!licenseNumber.value) {
    licenseNumberError.value = 'License number is required.'
    valid = false
  }
  
  if (valid) {
    isLoading.value = true
    try {
      // Format the phone number with Malaysia country code
      const formattedPhone = `+60${phone.value}`
      
      // Prepare driver data for registration
      const driverData = {
        name: username.value,
        email: email.value,
        phone: formattedPhone,
        password: password.value,
        licenseNumber: licenseNumber.value,
        carNumber: carPlate.value,
        carType: carType.value,
        carColour: carColor.value,
      }
      
      await userStore.registerDriver(driverData)
    } catch (error) {
      console.error('Driver registration error:', error)
    } finally {
      isLoading.value = false
    }
  }
}
</script>
