


// Function to fetch data from the API
async function fetchBusesData() {
    try {
        const response = await fetch('http://127.0.0.1:8000/vehicles/getallbusses');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
async function fetchBusData(licensePlate) {
    try {
        const url = `http://127.0.0.1:8000/vehicles/getvehicle?license_plate=${encodeURIComponent(licensePlate)}`;
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to render data in cards
async function renderBusData() {
    const container = document.getElementById('carousel-inner1'); // Change to your actual container ID
    container.classList.add('flex', 'transition-transform', 'duration-300', 'ease-in-out', 'h-40')
    const data = await fetchBusesData();
    // const busdata = await fetchBusData();

    // console.log(data.bus_list)
    

    if (!data) {
        return;
    }

    data.bus_list.forEach(bus => {
        let index = 0;
        const card = document.createElement('div');
        card.classList.add('card1', 'mx-4', 'shadow-md', 'relative');

        // Create elements for bus details (adjust as needed)
        const image = document.createElement('img');
        image.src = 'bus.png'; // Replace with actual image path or URL
        image.alt = '';
        image.classList.add('h-full')

        const span = document.createElement('span');
        span.classList.add('absolute', 'inset-x-0', 'bottom-0', 'bg-gradient-to-t', 'from-black', 'via-black', 'h-1/2', 'text-white', 'px-4', 'py-2');

        const descriptiveName = document.createElement('p');
        descriptiveName.textContent = bus.descriptive_name;

        const licensePlate = document.createElement('p');
        licensePlate.classList.add('text-sm');
        licensePlate.textContent = bus.license_plate;

        const link = document.createElement('button');
        link.classList.add( 'flex', 'justify-end', 'text-sm');
        link.textContent = 'View more';
        link.id = 'edit-' + bus.license_plate;
        // link.setAttribute("onclick", "return createEditModal(" + bus.license_plate + ")")
        link.onclick = function() {
            createEditModal(bus.license_plate);
        };
       
        span.appendChild(descriptiveName);
        span.appendChild(licensePlate);
        span.appendChild(link);

        card.appendChild(image);
        card.appendChild(span);
        container.appendChild(card);
    });

    const carousel1 = document.getElementById('carousel1');
const carousel2 = document.getElementById('carousel2');
const inner1 = document.getElementById('carousel-inner1');
const inner2 = document.getElementById('carousel-inner2');
let cards1 = document.querySelectorAll('.card1');
let cards2 = document.querySelectorAll('.card2');
let card1Width = cards1[0].offsetWidth + 8; // 8 for margin

console.log(cards1.length);
let currentIndex = 0;

function updateCarousel1() {
    // console.log('whoo');
    inner1.style.transform = `translateX(${-currentIndex * card1Width}px)`;
    // console.log();
}


function nextSlide1() {
    currentIndex = (currentIndex + 1) % cards1.length;
    updateCarousel1();
}
function nextSlide2() {
    currentIndex = (currentIndex + 1) % cards2.length;
    console.log(currentIndex);
    updateCarousel2();
}

function prevSlide1() {
    currentIndex = (currentIndex - 1 + cards1.length) % cards1.length;
    updateCarousel1();
}

function prevSlide2() {
    currentIndex = (currentIndex - 1 + cards2.length) % cards2.length;
    updateCarousel2();
}


// Add event listeners for next and previous buttons
document.getElementById('prev-btn1').addEventListener('click', prevSlide1);
document.getElementById('prev-btn2').addEventListener('click', prevSlide2);
document.getElementById('next-btn1').addEventListener('click', nextSlide1);
document.getElementById('next-btn2').addEventListener('click', nextSlide2);


}

// Call the renderBusData function to display data
renderBusData();


async function fetchCarsData() {
    try {
        const response = await fetch('http://127.0.0.1:8000/vehicles/getallprivate');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
async function fetchCarData(licensePlate) {
    try {
        const url = `http://127.0.0.1:8000/vehicles/getvehicle?license_plate=${encodeURIComponent(licensePlate)}`;
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to render data in cards
async function renderCarData() {
    const container = document.getElementById('carousel-inner2'); // Change to your actual container ID
    container.classList.add('flex', 'transition-transform', 'duration-300', 'ease-in-out', 'h-40')
    const data = await fetchCarsData();
    console.log(data)

    if (!data) {
        return;
    }

    data.private_list.forEach(car => {
        const card = document.createElement('div');
        card.classList.add('card1', 'mx-4', 'shadow-md', 'relative');

        const image = document.createElement('img');
        image.src = 'car.png'; 
        image.alt = '';
        image.classList.add('h-full')

        const span = document.createElement('span');
        span.classList.add('absolute', 'inset-x-0', 'bottom-0', 'bg-gradient-to-t', 'from-black', 'via-black', 'h-1/2', 'text-white', 'px-4', 'py-2');

        const descriptiveName = document.createElement('p');
        descriptiveName.textContent = car.descriptive_name;

        const licensePlate = document.createElement('p');
        licensePlate.classList.add('text-sm');
        licensePlate.textContent = car.license_plate;

        const link = document.createElement('button');
        link.classList.add( 'flex', 'justify-end', 'text-sm');
        link.textContent = 'View more';
        link.onclick = function() {
            createEditModal(car.license_plate);
        };

        // link.onclick = function() {
        //     console.log('ha');
        //     const editBus = document.getElementById('editBus');
        //     fetchCarData(car.license_plate).then(car => {
        //         document.getElementById('editTitle').textContent = 'Edit Vehicle Details'
        //         editBus.style.display='block';
                
        //         document.getElementById('name').value = car.descriptive_name;
        //         document.getElementById('license').value = car.license_plate;
        //         document.getElementById('issuer').value = car.permit_issuer;
        //         document.getElementById('issuerDate').value = car.permit_issue_date;
        //         document.getElementById('expiry').value = car.permit_expiry_date;
        //         // document.getElementById('last').value = car.last;
        //         // document.getElementById('next').value = car.next;
        //         document.getElementById('driver').value = car.assigned_driver;

        //         // For simplicity, you can use the bus data to populate the modal fields
        //         // editBusModal.innerHTML = `
        //         //     <p>Bus Name: ${bus.descriptive_name}</p>
        //         //     <p>License Plate: ${bus.license_plate}</p>
        //         //     <!-- Add other fields as needed -->
        //         //     <button onclick="editBusDetails('${bus.license_plate}')">Edit Details</button>
        //         // `;

        //     })
        //     .catch(error => {
        //         console.error('Error fetching bus data:', error);
        //     });
            
        // };

        span.appendChild(descriptiveName);
        span.appendChild(licensePlate);
        span.appendChild(link);

        card.appendChild(image);
        card.appendChild(span);
        container.appendChild(card);
    });

const carousel2 = document.getElementById('carousel2');
const inner2 = document.getElementById('carousel-inner2');
let cards2 = document.querySelectorAll('.card2');
let card2Width = cards2[0].offsetWidth + 8; // 8 for margin

let currentIndex = 0;


function updateCarousel2() {
    inner2.style.transform = `translateX(${-currentIndex * card2Width}px)`;
}

function nextSlide2() {
    currentIndex = (currentIndex + 1) % cards2.length;
    console.log(currentIndex);
    updateCarousel2();
}


function prevSlide2() {
    currentIndex = (currentIndex - 1 + cards2.length) % cards2.length;
    updateCarousel2();
}

function cloneFirstAndLastCards() {
    const firstCard = cards2[0].cloneNode(true);
    const lastCard = cards2[cards2.length - 1].cloneNode(true);

    inner2.appendChild(firstCard);
    inner2.insertBefore(lastCard, inner2.firstChild);

    let cardsArray = Array.from(cards2);

    // Push the cloned cards into the array
    cardsArray.push(firstCard, lastCard);

    // Update cards2 with the new array
    cards2 = document.querySelectorAll('.card2');}

cloneFirstAndLastCards();
updateCarousel2();

// Add event listeners for next and previous buttons
document.getElementById('prev-btn2').addEventListener('click', prevSlide2);
document.getElementById('next-btn2').addEventListener('click', nextSlide2);


}

// Call the renderData function to display data
renderCarData();


async function fetchDrivers() {
    try {
        const url = `http://127.0.0.1:8000/drivers/alldrivers`;
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
async function fetchBus(license) {
    try {
        const url = `http://127.0.0.1:8000/vehicles/getvehicle?license_plate=${license}`;
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}


async function createEditModal(license) {
    const busdata = await fetchBus(license)

    if (!busdata) {
        return;
    }

    // Create modal container
    const modalContainer = document.getElementById('page');

    // Create modal elements
    const modalOverlay = document.createElement('div');
    modalOverlay.classList.add( 'overscroll-none', 'absolute', 'inset-0', 'bg-black', 'bg-opacity-50');
    modalOverlay.id = 'editBus-'+ license;

    const modalContent = document.createElement('div');
    modalContent.classList.add('absolute', 'w-2/5', 'h-5/6', 'top-1/2', 'left-1/2', 'transform', '-translate-x-1/2', '-translate-y-1/2', 'bg-white', 'rounded-lg', 'overflow-y-auto');

    // Add close button
    const closeButton = document.createElement('button');
    closeButton.id = 'close';
    closeButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="#011936" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="m7 7l10 10M7 17L17 7"/></svg>';
    closeButton.addEventListener('click', function () {
        modalOverlay.classList.add('hidden');
    });

    const title = document.createElement('p');
    title.classList.add('flex', 'justify-center', 'mt-3', 'font-bold', 'text-2xl');
    title.id = 'editTitle';
    title.textContent = 'Edit Bus Details';

    const inner = document.createElement('div');
    inner.classList.add('flex', 'flex-col', 'ml-3', 'mr-3', 'mt-3');
    
    const editSpan = document.createElement('span');
    editSpan.classList.add('flex', 'justify-end', 'items-center');
    editSpan.id = 'editSpan-'+ license;

    const editIcon = document.createElement('svg');
    editIcon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    editIcon.classList.add('mr-1');
    editIcon.width = '18';
    editIcon.height = '24';
    editIcon.setAttribute('viewBox', '0 0 24 24');

    
    const editButton = document.createElement('button');
    editButton.type = 'edit';
    editButton.classList.add('shadow-lg', 'rounded-lg', 'items-center');
    editButton.id = 'edit-'+license;
    editButton.innerHTML += 'Edit Details';
    editButton.onclick = function() {
        console.log('hee');
        handleEdit(license);
        editButton.style.display = 'none';
    };
    // editButton.setAttribute("onclick", "return handleEdit(" + license + ")")


    const editIcon2 = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    
    editIcon2.setAttribute("width", "18");
    editIcon2.setAttribute("height", "24");
    editIcon2.setAttribute("viewBox", "0 0 24 24");
    editIcon2.id= 'editIcon-'+ license;

    const editPath2 = document.createElementNS("http://www.w3.org/2000/svg", "path");
    editPath2.setAttribute("fill", "#011936");
    editPath2.setAttribute("d", "M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04a.996.996 0 0 0 0-1.41l-2.34-2.34a.996.996 0 0 0-1.41 0l-1.83 1.83l3.75 3.75l1.83-1.83z");

    editIcon2.appendChild(editPath2);
    editButton.appendChild(editIcon2)


    const editForm = document.createElement('form');
    editForm.id = 'editUserDetailsForm';
    editForm.action = 'PATCH';
    console.log(editForm.id);

    function createFormElement(labelText, inputType, inputId, inputName, value, isDisabled = false) {
        const formDiv = document.createElement('div');
        formDiv.classList.add('mb-5');

        const label = document.createElement('label');
        label.setAttribute('for', inputId);
        label.textContent = labelText;

        const input = document.createElement('input');
        input.type = inputType;
        input.id = inputId;
        input.value = value;
        input.name = inputName;
        // input.required;
        // input.classList.add('form-control');
        if (isDisabled) {
            input.setAttribute('disabled', 'true');
        }

        formDiv.appendChild(label);
        formDiv.appendChild(input);

        return formDiv;
    }

    // Example form elements
    editForm.appendChild(createFormElement('Name:', 'text', 'name-'+license, 'descriptive_name', busdata.Vehicle_data.descriptive_name, true));
    editForm.appendChild(createFormElement('License Number:', 'text', 'license-'+license, 'license_plate', busdata.Vehicle_data.license_plate, true));
    editForm.appendChild(createFormElement('Capacity:', 'text', 'capacity-'+license, 'capacity', busdata.Vehicle_data.capacity, true));
    editForm.appendChild(createFormElement('Car Make:', 'text', 'make-'+license, 'make', busdata.Vehicle_data.make, true));
    editForm.appendChild(createFormElement('Car Model:', 'text', 'model-'+license, 'model', busdata.Vehicle_data.model, true));
    
    const permitInfo = document.createElement('p');
    permitInfo.textContent = 'Permit Information';
    permitInfo.classList.add('text-gray-500', 'font-semibold');
    
    editForm.appendChild(permitInfo);
    editForm.appendChild(createFormElement('Permit Issuer:', 'text', 'issuer-'+license, 'permit_issuer', busdata.Vehicle_data.permit_issuer, true));
    editForm.appendChild(createFormElement('Permit Issue Date:', 'date', 'issuerDate-'+license,'permit_issue_date', busdata.Vehicle_data.permit_issue_date, true));
    editForm.appendChild(createFormElement('Permit Expiry Date:', 'date', 'expiry-'+license, 'permit_expiry_date', busdata.Vehicle_data.permit_expiry_date, true));
    
    const mainInfo = document.createElement('p');
    mainInfo.textContent = 'Maintenance Information';
    mainInfo.classList.add('text-gray-500', 'font-semibold');
    
    editForm.appendChild(mainInfo);
    editForm.appendChild(createFormElement('Last Serviced on:', 'date', 'last-'+license, 'last_maintenance_date', busdata.Vehicle_data.last_maintenance_date,true));
    editForm.appendChild(createFormElement('Next Servicing Date:', 'date', 'next-'+license, 'next_maintenance_date', busdata.Vehicle_data.next_maintenance_date, true));

    const drivInfo = document.createElement('p');
    drivInfo.textContent = 'Assigned Driver';
    drivInfo.classList.add('text-gray-500', 'font-semibold');

    const driverDiv = document.createElement('div');
    
    const driverLabel = document.createElement('label');
    driverLabel.setAttribute('for', 'driver-'+license);
    driverLabel.textContent = 'Assigned Driver';
    
        const data = await fetchDrivers();
        if (!data) {
            return;
        }

    const dropdown = document.createElement('select');
    dropdown.classList.add('bg-gray-200');
    dropdown.id = 'driver-'+ license;
    dropdown.setAttribute("disabled", "");
    dropdown.name = 'assigned_driver';
    
    const firstoption = document.createElement('option');
    firstoption.value = busdata.Vehicle_data.assigned_driver;
    data.Drivers.forEach(driver => {
        if (driver.employee_id === firstoption.value){
            firstoption.textContent = driver.driver_fname + ' '+ driver.driver_lname;
            return
        }
    });

    dropdown.appendChild(firstoption);
    console.log(firstoption.value);
    

    data.Drivers.forEach(driver => {
        const option = document.createElement('option');
        option.value = driver.employee_id;
        option.textContent = driver.driver_fname + ' '+ driver.driver_lname
        dropdown.appendChild(option);
    });
    editForm.appendChild(drivInfo);
    driverDiv.appendChild(driverLabel);
    driverDiv.appendChild(dropdown);
    editForm.appendChild(driverDiv);

    const saveSpan= document.createElement('span');
    saveSpan.classList.add('flex', 'justify-end')

    const saveButton = document.createElement('button');
    saveButton.type = 'submit';
    saveButton.classList.add('flex', 'justify-end', 'items-center', 'mb-5');
    saveButton.id = 'save-'+license;
    saveButton.setAttribute("style", "display: none;");
    saveButton.onclick = function() {
        if(busdata.Vehicle_data.vehicle_type === "Bus"){

            handleSave(license);
        }
        else{handleCarSave(license);}
        editButton.style.display = 'block';

    };


    const saveIcon = document.createElement('svg');
    saveIcon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    saveIcon.classList.add('mr-1.5');
    saveIcon.width = '20';
    saveIcon.height = '24';
    saveIcon.setAttribute('viewBox', '0 0 24 24');

    const savePath = document.createElement('path');
    savePath.setAttribute('fill', '#011936');
    savePath.setAttribute('d', 'M17 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14c1.1 0 2-.9 2-2V7l-4-4zm-5 16c-1.66 0-3-1.34-3-3s1.34-3 3-3s3 1.34 3 3s-1.34 3-3 3zm3-10H5V5h10v4z');

    saveIcon.appendChild(savePath);
    // saveButton.appendChild(saveIcon);
    saveButton.innerHTML += 'Save Changes';

    saveSpan.appendChild(saveIcon);
    saveSpan.appendChild(saveButton);
    saveSpan.appendChild(editButton);

    driverDiv.appendChild(driverLabel);
    driverDiv.appendChild(dropdown);

    editSpan.appendChild(editIcon2);
    editSpan.appendChild(editButton);

    inner.appendChild(editSpan);
    inner.appendChild(editForm);
    inner.appendChild(saveSpan);

    modalContent.appendChild(closeButton);
    modalContent.appendChild(title);
    modalContent.appendChild(inner);

    modalOverlay.appendChild(modalContent);

    modalContainer.appendChild(modalOverlay);
}


