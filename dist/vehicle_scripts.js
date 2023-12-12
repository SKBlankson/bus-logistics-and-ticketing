


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

    console.log(data.bus_list)
    

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
        link.setAttribute("onclick", "return handleEdit(" + bus.license_plate + ")")
        // const uniqueId = `bus${index + 1}`;
        // link.id = uniqueId;
        // console.log(uniqueId);
        
        // const busdata = await fetchBusData();


        // Attach the event listener to open the modal
        link.onclick = function() {
            console.log('true');
            const editBus = document.getElementById('editBus');
            fetchBusData(bus.license_plate).then(bus => {
                editBus.style.display='block';
                
                document.getElementById('name').value = bus.descriptive_name;
                document.getElementById('license').value = bus.license_plate;
                document.getElementById('issuer').value = bus.permit_issuer;
                document.getElementById('issuerDate').value = bus.permit_issue_date;
                document.getElementById('expiry').value = bus.permit_expiry_date;
                // document.getElementById('last').value = bus.last;
                // document.getElementById('next').value = bus.next;
                document.getElementById('driver').value = bus.assigned_driver;

                // For simplicity, you can use the bus data to populate the modal fields
                // editBusModal.innerHTML = `
                //     <p>Bus Name: ${bus.descriptive_name}</p>
                //     <p>License Plate: ${bus.license_plate}</p>
                //     <!-- Add other fields as needed -->
                //     <button onclick="editBusDetails('${bus.license_plate}')">Edit Details</button>
                // `;

            })
            .catch(error => {
                console.error('Error fetching bus data:', error);
            });
            
            // openModal(uniqueId); // Pass the unique ID to the openModal function
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
let card2Width = cards2[0].offsetWidth + 8; // 8 for margin

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

// function cloneFirstAndLastCards() {
//     const firstCard = cards1[0].cloneNode(true);
//     const lastCard = cards1[cards1.length - 1].cloneNode(true);

//     inner1.appendChild(firstCard);
//     inner1.insertBefore(lastCard, inner1.firstChild);

//     let cardsArray = Array.from(cards1);

//     // Push the cloned cards into the array
//     cardsArray.push(firstCard, lastCard);

//     // Update cards1 with the new array
//     cards1 = document.querySelectorAll('.card1');}

// cloneFirstAndLastCards();
// updateCarousel1();

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
            console.log('ha');
            const editBus = document.getElementById('editBus');
            fetchCarData(car.license_plate).then(car => {
                document.getElementById('editTitle').textContent = 'Edit Vehicle Details'
                editBus.style.display='block';
                
                document.getElementById('name').value = car.descriptive_name;
                document.getElementById('license').value = car.license_plate;
                document.getElementById('issuer').value = car.permit_issuer;
                document.getElementById('issuerDate').value = car.permit_issue_date;
                document.getElementById('expiry').value = car.permit_expiry_date;
                // document.getElementById('last').value = car.last;
                // document.getElementById('next').value = car.next;
                document.getElementById('driver').value = car.assigned_driver;

                // For simplicity, you can use the bus data to populate the modal fields
                // editBusModal.innerHTML = `
                //     <p>Bus Name: ${bus.descriptive_name}</p>
                //     <p>License Plate: ${bus.license_plate}</p>
                //     <!-- Add other fields as needed -->
                //     <button onclick="editBusDetails('${bus.license_plate}')">Edit Details</button>
                // `;

            })
            .catch(error => {
                console.error('Error fetching bus data:', error);
            });
            
            // openModal(uniqueId); // Pass the unique ID to the openModal function
        };

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


