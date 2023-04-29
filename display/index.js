const mapContainer = document.getElementById("map")

let regionList = [
	"VERY_NORTH_WEST",
	"NORTH_EAST",
	"NORTH",
	"NORTH_WEST",
	"VERY_NORTH_EAST",
	"WEST",
	"MIDDLE_WEST",
	"CENTRAL",
	"MIDDLE_EAST",
	"EAST",
	"VERY_SOUTH_WEST",
	"SOUTH_WEST",
	"SOUTH",
	"SOUTH_EAST",
	"VERY_SOUTH_EAST",
];

function createPersonDisplayButton(PersonID, PersonName) {
	return `<button onclick="showPersonInfo('${PersonID}')">${PersonName}</button>`;
}

function showPersonInfo(personID) {
	console.log(data.people[personID]);
}

function createDataSpan(title, info) {
	return `<p class="data-line"><span class="title">${title}  👉</span> ${info}</p>`;
}

// displaying names of regions
output = ``
for (let i = 0; i<3; i++) {
	output += `<div class="region-container ${["north", "central", "south"][i]}-regions">`
	for (r of data.regions_coord[i]) {
		output += `<div class="show-region-button" onclick="showRegionData(this)">${r}</div>`
	}
	output += `</div>`
}

mapContainer.innerHTML = output;


for (region of regionList) {
	let regionData = data[region];

	console.log(regionData);
}

