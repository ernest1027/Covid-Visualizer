let map;
let service;
let infoWindow;
var initLoc;
const locations = {
  AN: { name: "Andaman And Nicobar ", lat: 11.66702557, lon: 92.73598262 },
  AP: { name: "Andhra Pradesh ", lat: 14.7504291, lon: 78.57002559 },
  AR: { name: "Arunachal Pradesh ", lat: 27.10039878, lon: 93.61660071 },
  AS: { name: "Assam ", lat: 26.7499809, lon: 94.21666744 },
  BR: { name: "Bihar ", lat: 25.78541445, lon: 87.4799727 },
  CH: { name: "Chandigarh ", lat: 30.71999697, lon: 76.78000565 },
  CT: { name: "Chhattisgarh ", lat: 22.09042035, lon: 82.15998734 },
  DL: { name: "Delhi ", lat: 28.6699929, lon: 77.23000403 },
  GA: { name: "Goa ", lat: 15.491997, lon: 73.81800065 },
  GJ: { name: "Gujarat ", lat: 22.2587, lon: 71.1924 },
  HR: { name: "Haryana ", lat: 28.45000633, lon: 77.01999101 },
  HP: { name: "Himachal Pradesh ", lat: 31.10002545, lon: 77.16659704 },
  JK: { name: "Jammu And Kashmir ", lat: 34.29995933, lon: 74.46665849 },
  JH: { name: "Jharkhand ", lat: 23.80039349, lon: 86.41998572 },
  KA: { name: "Karnataka ", lat: 12.57038129, lon: 76.91999711 },
  KL: { name: "Kerala ", lat: 8.900372741, lon: 76.56999263 },
  LD: { name: "Lakshadweep ", lat: 10.56257331, lon: 72.63686717 },
  LA: { name: "Ladakh ", lat: 34.2268, lon: 77.5619 },
  MP: { name: "Madhya Pradesh ", lat: 21.30039105, lon: 76.13001949 },
  MH: { name: "Maharashtra ", lat: 19.25023195, lon: 73.16017493 },
  MN: { name: "Manipur ", lat: 24.79997072, lon: 93.95001705 },
  ML: { name: "Meghalaya ", lat: 25.57049217, lon: 91.8800142 },
  MZ: { name: "Mizoram ", lat: 23.71039899, lon: 92.72001461 },
  NL: { name: "Nagaland ", lat: 25.6669979, lon: 94.11657019 },
  OR: { name: "Orissa ", lat: 19.82042971, lon: 85.90001746 },
  PY: { name: "Puducherry ", lat: 11.93499371, lon: 79.83000037 },
  PB: { name: "Punjab ", lat: 31.51997398, lon: 75.98000281 },
  RJ: { name: "Rajasthan ", lat: 26.44999921, lon: 74.63998124 },
  SK: { name: "Sikkim ", lat: 27.3333303, lon: 88.6166475 },
  TN: { name: "Tamil Nadu ", lat: 12.92038576, lon: 79.15004187 },
  TG: { name: "Telangana ", lat: 18.1124, lon: 79.0193 },
  TR: { name: "Tripura ", lat: 23.83540428, lon: 91.27999914 },
  UP: { name: "Uttar Pradesh ", lat: 27.59998069, lon: 78.05000565 },
  UT: { name: "Uttaranchal ", lat: 30.32040895, lon: 78.05000565 },
  WB: { name: "West Bengal ", lat: 22.58039044, lon: 88.32994665 },
};

let data = {};

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 5,
    center: { lat: 10, lng: 78.9 },
  });
}

function setMarkers() {
  infoWindow = new google.maps.InfoWindow();
  // Create the markers.
  Object.keys(locations).forEach((state, i) => {
    let position = { lat: locations[state].lat, lng: locations[state].lon };
    let title = locations[state].name;
    const marker = new google.maps.Marker({
      position,
      map,
      title: `${title}`,
      label: state,
      optimized: false,
    });
    // Add a click listener for each marker, and set up the info window.
    google.maps.event.addListener(infoWindow, "closeclick", goBack);
    marker.addListener("click", () => {
      infoWindow.close();
      infoWindow.setContent(marker.getTitle());
      infoWindow.open(marker.getMap(), marker);

      
      document.getElementById("totalContent").innerHTML = "";
      axios.get(`https://v-map-hackon.herokuapp.com/chart?location=${marker.getLabel()}&days=${document.getElementById("myRange").value}&vaccine=${vaccine_num}`).then((response) => {
        console.log(response.data);
        var graphs = response.data;
        Plotly.plot("chart", graphs, {});
      });
      let e = document.getElementById("myRange").value
      document.getElementById("stateContent").innerHTML =(`
      <h2>${marker.getTitle()}</h2>
      <p>Susceptible: ${data[e][state]["susceptible"]}</p>
      <p>Infected: ${data[e][state]["infected"]}</p>
      <p>Recovered: ${data[e][state]["recovered"]}</p>
      <p>Deceased: ${data[e][state]["dead"]}</p>
      <button class="btn btn-secondary" onclick="goBack()">Go Back</button>
      <br></br>
      <div id="chart" class="chart"></div>
      
      `);
    });
  });
}
function showstatstable(){
  document.getElementById("statstable").classList.toggle("hidden");
  if(document.getElementById("showStats").innerHTML == "Hide stats table")
  {
    document.getElementById("showStats").innerHTML = "Show stats table"
  }
  else{
    document.getElementById("showStats").innerHTML = "Hide stats table"
  }
  
}

function goBack() {
  if (
    document.getElementById("stateContent").innerHTML !=
    '<div id="chart" class="chart"></div> '
  ) {
    setHeatMap(document.getElementById("myRange").value);
  }
  document.getElementById("stateContent").innerHTML =
    '<div id="chart" class="chart"></div> ';
}

function setHeatMap(e) {
  infoWindow.close()
  document.getElementById("stateContent").innerHTML = '<div id="chart" class="chart"></div> ';
  let heatmapData = [];
  let content = `
  <button class ="btn btn-secondary" id="showStats" onclick="showstatstable()">Hide stats table</button>
  <br></br>
    <table id="statstable" class="table table-sm ">
      <thead class="thead-dark">
        <tr>
          <th scope="col">State</th>
          <th scope="col">Susceptible</th>
          <th scope="col">Infected</th>
          <th scope="col">Recovered</th>
          <th scope="col">Vaccinated</th>
          <th scope="col">Deceased</th>
          <td>
        </tr>
      </thead>
      <tbody>
    
  
  
  `;
  Object.keys(locations).forEach((state, i) => {
    heatmapData.push({
      location: new google.maps.LatLng(
        locations[state].lat,
        locations[state].lon
      ),
      weight: data[e][state]["infected"],
      // weight: (data[e][state]["infected"]/(data[e][state]["infected"]+data[e][state]["recovered"]+data[e][state]["susceptible"]))*1000
    });
    content += `
    <tr>
      <th scope="row">${locations[state].name}</th>
      <td>${data[e][state]["susceptible"]}</td>
      <td>${data[e][state]["infected"]}</td>
      <td>${data[e][state]["recovered"]}</td>
      <td>${Math.floor(data[e][state]["vaccinated"])}</td>
      <td>${data[e][state]["dead"]}</td>
    
  </tr>
    
    `;
  });
  content += " </tbody></table>"
  let heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatmapData,
  });
  heatmap.setOptions({ radius: "30" });
  heatmap.setMap(map);
  document.getElementById("totalContent").innerHTML = content;
}

document
  .getElementById("vaccineForm")
  .addEventListener("submit", vaccineSubmit);
let vaccine_num
function vaccineSubmit(e) {
  e.preventDefault();
  if (isNaN(document.getElementById("vaccines").value) || document.getElementById("vaccines").value === "") {
    window.alert("Please enter a number");
  } else {
    //get data from python
    vaccine_num = document.getElementById("vaccines").value
    axios
      .get(
        `https://v-map-hackon.herokuapp.com/calc?vaccine=${
          document.getElementById("vaccines").value
        }&days=90`
      )
      .then((response) => {
        data = response.data;
        console.log(data);
        setMarkers();
        setHeatMap(0);
      });
    //Make slider
    document.getElementById("content").innerHTML = `
      <button onClick="window.location.reload();" class="btn btn-secondary">Restart</button>
        <label for="myRange" id="myRangeValue">Prediction for 60 days in the future</label>
       <input type="range" min="0" max="89" value="60" class="form-range" id="myRange" oninput="changeRange(this.value)" onchange="setHeatMap(this.value)">
       <div id=stateContent>
        <div id="chart" class="chart"></div>     
       </div> 
       <div id = totalContent> </div>             
       `;
  }
}

function changeRange(e){
  console.log(e)
  document.getElementById("myRangeValue").innerHTML = `Time Elapsed (in Days) ${e}`
}
