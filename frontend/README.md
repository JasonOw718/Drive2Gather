# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).

# Ride2Gather Admin Panel – Project Structure & Routing Guide

🚀 Running the Frontend
<pre>cd frontend</pre>
<pre>npm install</pre>
<pre>npm run serve</pre>
## 📁 Project Structure Overview

All main source files are under `Ride2Gather/src/`.

---

## 🗺️ Routing Structure

The routing is defined in [`Ride2Gather/src/router/index.js`](Ride2Gather/src/router/index.js).  
The admin panel uses nested routes under `/admin`, with each page as a child route.

### Main Admin Routes

| Route Path                        | Vue File Location                                                                 | Purpose                                                                                 |
|------------------------------------|----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| `/admin/driver-registration`       | [`Ride2Gather/src/components/pages/admin/component/DriverRegistrationList.vue`](Ride2Gather/src/components/pages/admin/component/DriverRegistrationList.vue) | Shows a list of drivers pending registration approval.                                  |
| `/admin/driver-management`         | [`Ride2Gather/src/components/pages/admin/component/DriverManagement.vue`](Ride2Gather/src/components/pages/admin/component/DriverManagement.vue) | (Assumed) For managing all registered drivers.                                          |
| `/admin/driver-detail/:id`         | [`Ride2Gather/src/components/pages/admin/component/DriverDetails.vue`](Ride2Gather/src/components/pages/admin/component/DriverDetails.vue) | Shows detailed info for a specific driver, including car and license photos.            |
| `/admin/report-list`               | [`Ride2Gather/src/components/pages/admin/component/ReportList.vue`](Ride2Gather/src/components/pages/admin/component/ReportList.vue) | Shows a list of all reports submitted, sorted by date.                                  |
| `/admin/report-detail/:id`         | [`Ride2Gather/src/components/pages/admin/component/ReportDetails.vue`](Ride2Gather/src/components/pages/admin/component/ReportDetails.vue) | Shows detailed info for a specific report.                                              |

> **Note:** The main admin layout is in [`Ride2Gather/src/components/pages/admin/AdminLayout.vue`](Ride2Gather/src/components/pages/admin/AdminLayout.vue), which provides the sidebar and header for all admin pages.

---

## 📝 Page Purposes & Descriptions

### [`DriverRegistrationList.vue`](Ride2Gather/src/components/pages/admin/component/DriverRegistrationList.vue)
- **Purpose:**  
  Displays a list of drivers with `status: 'pending'` for admin review.  
  Each row has a "Details" button to view more info about the driver.
- **Data Source:**  
  Fetches mock driver data from [`Ride2Gather/src/components/stores/driver.js`](Ride2Gather/src/components/stores/driver.js).

### [`DriverDetails.vue`](Ride2Gather/src/components/pages/admin/component/DriverDetails.vue)
- **Purpose:**  
  Shows all details for a selected driver, including name, phone, email, car info, profile picture, license images, and car photos.  
  Admin can approve or reject the driver.
- **Data Source:**  
  Fetches driver details by ID from [`Ride2Gather/src/components/stores/driver.js`](Ride2Gather/src/components/stores/driver.js).

### [`DriverManagement.vue`](Ride2Gather/src/components/pages/admin/component/DriverManagement.vue)
- **Purpose:**  
  (Assumed) For managing all drivers (not just pending).  
  **Check this file for more details if implemented.**
- **Data Source:**  
  Likely uses [`Ride2Gather/src/components/stores/driver.js`](Ride2Gather/src/components/stores/driver.js).

### [`ReportList.vue`](Ride2Gather/src/components/pages/admin/component/ReportList.vue)
- **Purpose:**  
  Displays a list of all reports, sorted by date (ascending).  
  Each row has a "Detail" button to view the full report.
- **Data Source:**  
  Fetches mock report data from [`Ride2Gather/src/components/stores/report.js`](Ride2Gather/src/components/stores/report.js).

### [`ReportDetails.vue`](Ride2Gather/src/components/pages/admin/component/ReportDetails.vue)
- **Purpose:**  
  Shows all details for a selected report, including driver name, date, status, issue, and details.
- **Data Source:**  
  Fetches report details by ID from [`Ride2Gather/src/components/stores/report.js`](Ride2Gather/src/components/stores/report.js).

### [`AdminLayout.vue`](Ride2Gather/src/components/pages/admin/AdminLayout.vue)
- **Purpose:**  
  Provides the sidebar navigation and header for all admin pages.  
  Handles route switching and sign out.

---

## 📦 Mock Data Sources

- **Drivers:**  
  All driver-related mock data is in [`Ride2Gather/src/components/stores/driver.js`](Ride2Gather/src/components/stores/driver.js).
- **Reports:**  
  All report-related mock data is in [`Ride2Gather/src/components/stores/report.js`](Ride2Gather/src/components/stores/report.js).

---

## 🛣️ How Routing Works

- The main router is set up in [`Ride2Gather/src/router/index.js`](Ride2Gather/src/router/index.js).
- The `/admin` route uses [`AdminLayout.vue`](Ride2Gather/src/components/pages/admin/AdminLayout.vue) as a layout, with all admin pages as its children.
- Each admin page is mapped to a specific path and component as shown above.
- Navigation between pages (e.g., clicking "Details" or "Detail" buttons) uses Vue Router's named routes and passes the relevant `id` as a route param.

---

## 🧑‍💻 How to Find a Page

- **To view or edit a page:**  
  Click the file path in this document (e.g., [`DriverDetails.vue`](Ride2Gather/src/components/pages/admin/component/DriverDetails.vue)) to jump directly to the file in your editor.

- **To update mock data:**  
  Edit the relevant store file:  
  - Drivers: [`driver.js`](Ride2Gather/src/components/stores/driver.js)  
  - Reports: [`report.js`](Ride2Gather/src/components/stores/report.js)

---

## 📝 ADMIN Summary Table

| Page Name                | File Path                                                                 | Data Source File                                                      |
|--------------------------|--------------------------------------------------------------------------|-----------------------------------------------------------------------|
| Driver Registration List | [`DriverRegistrationList.vue`](Ride2Gather/src/components/pages/admin/component/DriverRegistrationList.vue) | [`driver.js`](Ride2Gather/src/components/stores/driver.js)            |
| Driver Details           | [`DriverDetails.vue`](Ride2Gather/src/components/pages/admin/component/DriverDetails.vue) | [`driver.js`](Ride2Gather/src/components/stores/driver.js)            |
| Driver Management        | [`DriverManagement.vue`](Ride2Gather/src/components/pages/admin/component/DriverManagement.vue) | [`driver.js`](Ride2Gather/src/components/stores/driver.js)            |
| Report List              | [`ReportList.vue`](Ride2Gather/src/components/pages/admin/component/ReportList.vue) | [`report.js`](Ride2Gather/src/components/stores/report.js)            |
| Report Details           | [`ReportDetails.vue`](Ride2Gather/src/components/pages/admin/component/ReportDetails.vue) | [`report.js`](Ride2Gather/src/components/stores/report.js)            |
| Admin Layout             | [`AdminLayout.vue`](Ride2Gather/src/components/pages/admin/AdminLayout.vue) | N/A (Layout only)                                                     |

---

🚗 Passenger & Driver Side Pages
Routing Overview
The main routes for passenger and driver pages are also defined in `Ride2Gather/src/router/index.js`.
These routes are mapped to their respective Vue components under the /components/pages/passanger/ and /components/pages/driver/ directories.
Passenger Pages
| Route Path | Vue File Location | Purpose | Data Source File |
|---------------------------|----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| /find-ride | `Ride2Gather/src/components/pages/passanger/FindRide.vue` | Allows passengers to search for available rides. | `Ride2Gather/src/components/stores/ride.js` |
| /ride-list | `Ride2Gather/src/components/pages/passanger/RideList.vue` | Displays a list of rides available to the passenger. | `Ride2Gather/src/components/stores/ride.js` |
| /ride-detail | `Ride2Gather/src/components/pages/passanger/RideDetail.vue` | Shows detailed information about a selected ride. | `Ride2Gather/src/components/stores/ride.js` |
| /ridebooked | `Ride2Gather/src/components/pages/passanger/Ridebooked.vue` | Shows the passenger's booked rides. | `Ride2Gather/src/components/stores/ride.js` |
| /otw | `Ride2Gather/src/components/pages/passanger/Otwpage.vue` | Displays the \"On The Way\" status for a booked ride. | `Ride2Gather/src/components/stores/ride.js` |
| /ride-complete | `Ride2Gather/src/components/pages/passanger/RidecompleteP.vue` | Shows the ride completion page for passengers. | `Ride2Gather/src/components/stores/ride.js` |
| /profile-passenger | `Ride2Gather/src/components/pages/passanger/ProfileP.vue` | Displays the passenger's profile information. | `Ride2Gather/src/components/stores/user.js` |
| /change-password | `Ride2Gather/src/components/pages/passanger/ChangePassword.vue` | Allows the passenger to change their password. | `Ride2Gather/src/components/stores/user.js` |
| /donation | `Ride2Gather/src/components/pages/passanger/Donation.vue` | Donation page for passengers. | `Ride2Gather/src/components/stores/donation.js` |
| /donate-complete | `Ride2Gather/src/components/pages/passanger/donatecomplete.vue` | Shows donation completion status. | `Ride2Gather/src/components/stores/donation.js` |
| /Reportpage | `Ride2Gather/src/components/pages/passanger/Report_Psg.vue` | Allows passengers to submit a report. | `Ride2Gather/src/components/stores/report.js` |
| /login-register | `Ride2Gather/src/components/pages/passanger/LoginRegister.vue` | Combined login/register page for passengers. | `Ride2Gather/src/components/stores/user.js` |
| /login | `Ride2Gather/src/components/pages/passanger/Login.vue` | Login page for passengers. | `Ride2Gather/src/components/stores/user.js` |
| /forgot-password | `Ride2Gather/src/components/pages/passanger/ForgotPassword.vue` | Password recovery for passengers. | `Ride2Gather/src/components/stores/user.js` |
| /register-passenger | `Ride2Gather/src/components/pages/passanger/RegisterP.vue` | Registration page for new passengers. | `Ride2Gather/src/components/stores/user.js` |

---

Driver Pages
| Route Path | Vue File Location | Purpose | Data Source File |
|---------------------------|----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| /create-ride | `Ride2Gather/src/components/pages/driver/CreateRide.vue` | Allows drivers to create a new ride. | `Ride2Gather/src/components/stores/ride.js` |
| /profile-driver | `Ride2Gather/src/components/pages/driver/ProfileD.vue` | Displays the driver's profile information. | `Ride2Gather/src/components/stores/user.js` |
| /register-driver | `Ride2Gather/src/components/pages/driver/RegisterD.vue` | Registration page for new drivers. | `Ride2Gather/src/components/stores/user.js` |
| /ride-detail-driverside | `Ride2Gather/src/components/pages/driver/RideDetailD.vue` | Shows ride details from the driver's perspective. | `Ride2Gather/src/components/stores/ride.js` |
| /dropoff | `Ride2Gather/src/components/pages/driver/Dropoff.vue` | Page for drivers to confirm passenger drop-off. | `Ride2Gather/src/components/stores/ride.js` |
| /ridecomplete-driver | `Ride2Gather/src/components/pages/driver/RidecompleteD.vue` | Shows ride completion page for drivers. | `Ride2Gather/src/components/stores/ride.js` |
| /Reportpage-driver | `Ride2Gather/src/components/pages/driver/Report_D_side.vue` | Allows drivers to submit a report. | `Ride2Gather/src/components/stores/report.js` |

---

🗂️ Mock Data Sources for Passenger & Driver
Rides:
All ride-related mock data is in `Ride2Gather/src/components/stores/ride.js`.
Users (Passenger/Driver):
All user-related mock data is in `Ride2Gather/src/components/stores/user.js`.
Reports:
All report-related mock data is in `Ride2Gather/src/components/stores/report.js`.
Donations:
All donation-related mock data is in `Ride2Gather/src/components/stores/donation.js`.

---

📝 How to Find and Edit Pages
To view or edit a page:
Click the file path in this document (e.g., `FindRide.vue`) to jump directly to the file in your editor.
To update mock data:
Edit the relevant store file:
Rides: `ride.js`
Users: `user.js`
Reports: `report.js`
Donations: `donation.js`

---

🧭 Summary Table: Passenger & Driver Pages
| Page Name | File Path | Data Source File |
|--------------------------|--------------------------------------------------------------------------|-----------------------------------------------------------------------|
| Find Ride | `FindRide.vue` | `ride.js` |
| Ride List | `RideList.vue` | `ride.js` |
| Ride Detail (Passenger) | `RideDetail.vue` | `ride.js` |
| Ride Booked | `Ridebooked.vue` | `ride.js` |
| On The Way | `Otwpage.vue` | `ride.js` |
| Ride Complete (Passenger)| `RidecompleteP.vue` | `ride.js` |
| Passenger Profile | `ProfileP.vue` | `user.js` |
| Change Password | `ChangePassword.vue` | `user.js` |
| Donation | `Donation.vue` | `donation.js` |
| Donate Complete | `donatecomplete.vue` | `donation.js` |
| Passenger Report | `Report_Psg.vue` | `report.js` |
| Login/Register | `LoginRegister.vue` | `user.js` |
| Login | `Login.vue` | `user.js` |
| Forgot Password | `ForgotPassword.vue` | `user.js` |
| Register Passenger | `RegisterP.vue` | `user.js` |
| Create Ride | `CreateRide.vue` | `ride.js` |
| Driver Profile | `ProfileD.vue` | `user.js` |
| Register Driver | `RegisterD.vue` | `user.js` |
| Ride Detail (Driver) | `RideDetailD.vue` | `ride.js` |
| Dropoff | `Dropoff.vue` | `ride.js` |
| Ride Complete (Driver) | `RidecompleteD.vue` | `ride.js` |
| Driver Report | `Report_D_side.vue` | `report.js` |
