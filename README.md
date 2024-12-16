# Database Final Project - Clinic Box

<br>

**Group:** Group 4

**Students:** 
- Ella Raputri (2702298154)
- Farrell Sevillen Arya (2702323540)
- Monish Haresh Giani (2702387834)

<br>

## Project Description
Clinic Box is a clinic appointment system used for patients to book their appointments with the doctors, doctors to see their appointments with the patients, and admins to see the overall bookings of their branch. 

<br>

## Documentation
To access the full documentation (document and images) and description for each page in detail, please refer to the 'documentation' folder inside this repository.

<br>

## Features and Screenshots
<details>
<summary>&ensp;<b>Login and Register</b></summary>

- Login is the first page that the user accesses when opening this app.

- From here, the user can choose to Register or Login. 

- User can login as an admin, doctor, or patient.

- If user chooses register, user can only register as a patient the doctors will be added by the branch admin, while the branch admin is added by the database administrator. 

- Here are some images for this feature:
  <img src="documentation\README_images\login.png" alt ="Login" width = "600"><br>
  <img src="documentation\README_images\register.png" alt="Register" width = "600"><br>
</details>

<br> 

<details>
<summary>&ensp;<b>Admin Section</b></summary>

- There are 4 separate pages for the admin section, which are Home Page, Doctor Page, Patient Page, and Booking Page. 

-  In the Admin Home Page (Admin Dashboard), the admin can see the information on booking and doctors for their corresponding branch. 

- On the Admin Doctor Page, the admin can see a table with basic information of each doctor in their branch. When a record is clicked, the schedule of that doctor is also shown in the schedule panel on the right side. Admin can also view the list of specialties here.

- Admin Patient Page is similar to Admin Doctor Page, but instead of doctors, it displays the patient data and allows filtering. It also displays the type of disease and the medical history of each patient. 

- Admin Booking Page displays the booking data in a tabular format and allows admins to edit it.

- Here are some of the images of this section:
  <img src="documentation\README_images\Admin\admin_dashboard.png" alt ="Admin Dashboard" width = "600"><br>
  <img src="documentation\README_images\Admin\admin_doctor.png" alt ="Admin Doctor" width = "600"><br>
  <img src="documentation\README_images\Admin\admin_patients.png" alt ="Admin Patient" width = "600"><br>
  <img src="documentation\README_images\Admin\admin_bookings.png" alt ="Admin Booking" width = "600"><br>
</details>

<br> 
<details>
<summary>&ensp;<b>Doctor Section</b></summary>

- There are 3 separate pages for the doctor section, which are Home Page, History Page, and Profile Page. 

-  On the Home Page, the doctor can see how many patients they have today, what are today’s booking, the current time, and pending patients (patients that have not met the doctor yet).

- The History Page displays all appointments the doctor has received regardless of the status, whether they are still pending, already completed, or canceled. It also displays the medical history of the selected patient.

- The Profile Page consists of the information of the doctor. The doctor can edit their personal information, from name to address details here. 

- Here are some of the images of this section:
  <img src="documentation\README_images\Doctor\home.png" alt ="Doctor Home" width = "600"><br>
  <img src="documentation\README_images\Doctor\history.png" alt ="Doctor History" width = "600"><br>
  <img src="documentation\README_images\Doctor\profile.png" alt ="Doctor Profile" width = "600"><br>
</details>

<br> 
<details>
<summary>&ensp;<b>Patient Section</b></summary>

- There are 3 separate pages for the patient section, which are Home Page, Booking Page, and History Page. 

-  On the Home Page, users can view and edit their personal information. They can also see their medical history and next appointment.

- On the Booking Page, patients can find doctors based on their branch or specialty and book an appointment with them.  

- The History Page contains the booking history of this patient with various doctors.

- Here are some of the images of this section:
  <img src="documentation\README_images\Patient\home.png" alt ="Patient Home" width = "600"><br>  <img src="documentation\README_images\Patient\search_book_dr.png" alt ="Patient Book Doctors" width = "600"><br>
  <img src="documentation\README_images\Patient\history.png" alt ="Patient History" width = "600"><br>
</details>