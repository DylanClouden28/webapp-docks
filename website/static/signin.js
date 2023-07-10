const testData = [
  { boatReg: 'AB123', phoneNumber: '1234567890', boatName: 'Sea Dream' },
  { boatReg: 'CD456', phoneNumber: '0987654321', boatName: 'Ocean Explorer' },
  { boatReg: 'EF789', phoneNumber: '1112223333', boatName: 'Sunset Cruise' },
  { boatReg: 'GH901', phoneNumber: '4445556666', boatName: 'Wave Rider' },
  { boatReg: 'IJ234', phoneNumber: '7778889990', boatName: 'Sailor\'s Delight' },
  { boatReg: 'KL567', phoneNumber: '2468101213', boatName: 'Aqua Adventure' },
  { boatReg: 'MN890', phoneNumber: '9876543210', boatName: 'Horizon Hopper' },
  { boatReg: 'OP123', phoneNumber: '1357924680', boatName: 'Marina Marvel' },
  { boatReg: 'QR456', phoneNumber: '8642097531', boatName: 'Nautical Nomad' },
  { boatReg: 'ST789', phoneNumber: '1029384756', boatName: 'Voyage Venture' },
  { boatReg: 'UV901', phoneNumber: '5678901234', boatName: 'Seafarer\'s Sanctuary' },
  { boatReg: 'WX234', phoneNumber: '3456789012', boatName: 'Coastal Cruiser' },
  { boatReg: 'YZ567', phoneNumber: '6789012345', boatName: 'Harbor Haven' },
  { boatReg: 'A1B2C3', phoneNumber: '9012345678', boatName: 'Port Paradise' },
  { boatReg: 'D4E5F6', phoneNumber: '2345678901', boatName: 'Tide Traveler' },
  { boatReg: 'G7H8I9', phoneNumber: '7654321098', boatName: 'Wind Wanderer' },
  { boatReg: 'J0K1L2', phoneNumber: '0981234567', boatName: 'Current Companion' },
  { boatReg: 'M3N4O5', phoneNumber: '3210987654', boatName: 'Reef Roamer' },
  { boatReg: 'P6Q7R8', phoneNumber: '5432109876', boatName: 'Bay Bounder' },
  { boatReg: 'S9T0U1', phoneNumber: '8765432109', boatName: 'Gulf Glider' },
];


const boatRegInput = document.getElementById('boat-reg');
const phoneNumberInput = document.getElementById('phone-number');
const boatNameInput = document.getElementById('boat-name');
const resultsTableBody = document.getElementById('results').getElementsByTagName('tbody')[0];

const homeButton = document.getElementById('home-btn');

function search() {
    const boatReg = boatRegInput.value;
    const phoneNumber = phoneNumberInput.value;
    const boatName = boatNameInput.value;

    // Filter test data using input values
    const filteredData = testData.filter(item =>
        (!boatReg || item.boatReg.includes(boatReg)) &&
        (!phoneNumber || item.phoneNumber.includes(phoneNumber)) &&
        (!boatName || item.boatName.toLowerCase().includes(boatName.toLowerCase()))
    );

    resultsTableBody.innerHTML = '';

    filteredData.forEach(item => {
        const newRow = resultsTableBody.insertRow();
        newRow.classList.add('boat-info-row');
      
        const boatRegCell = newRow.insertCell();
        boatRegCell.appendChild(createBoatInfoLink(item, item.boatReg));
      
        const phoneNumberCell = newRow.insertCell();
        phoneNumberCell.appendChild(createBoatInfoLink(item, item.phoneNumber));
      
        const boatNameCell = newRow.insertCell();
        boatNameCell.appendChild(createBoatInfoLink(item, item.boatName));
      });
}

boatRegInput.addEventListener('input', search);
phoneNumberInput.addEventListener('input', search);
boatNameInput.addEventListener('input', search);

function createBoatInfoLink(item, text) {
    const link = document.createElement('a');
    link.href = `boatdetails.html?boatReg=${item.boatReg}&phoneNumber=${item.phoneNumber}&boatName=${encodeURIComponent(item.boatName)}`;
    link.classList.add('boat-info-link');
    link.innerText = text;
    return link;
  }

homeButton.addEventListener('click', () => {
    window.location.href = 'index.html';
});

search();
