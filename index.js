let map;
let service;
let infowindow;
var initLoc;
const locations = 
    {"Meghalaya ": {"lat": 25.57049217, "lon": 91.8800142, "name": "Meghalaya "}, "Andhra Pradesh ": {"lat": 14.7504291, "lon": 78.57002559, "name": "Andhra Pradesh "}, "Jharkhand ": {"lat": 23.80039349, "lon": 86.41998572, "name": "Jharkhand "}, "Sikkim ": {"lat": 27.3333303, "lon": 88.6166475, "name": "Sikkim "}, "Rajasthan ": {"lat": 26.44999921, "lon": 74.63998124, "name": "Rajasthan "}, "Punjab ": {"lat": 31.51997398, "lon": 75.98000281, "name": "Punjab "}, "Karnataka ": {"lat": 12.57038129, "lon": 76.91999711, "name": "Karnataka "}, "West Bengal ": {"lat": 22.58039044, "lon": 88.32994665, "name": "West Bengal "}, "Nagaland ": {"lat": 25.6669979, "lon": 94.11657019, "name": "Nagaland "}, "Haryana ": {"lat": 28.45000633, "lon": 77.01999101, "name": "Haryana "}, "Puducherry ": {"lat": 11.93499371, "lon": 79.83000037, "name": "Puducherry "}, "Chhattisgarh ": {"lat": 22.09042035, "lon": 82.15998734, "name": "Chhattisgarh "}, "Delhi ": {"lat": 28.6699929, "lon": 77.23000403, "name": "Delhi "}, "Orissa ": {"lat": 19.82042971, "lon": 85.90001746, "name": "Orissa "}, "Manipur ": {"lat": 24.79997072, "lon": 93.95001705, "name": "Manipur "}, "Himachal Pradesh ": {"lat": 31.10002545, "lon": 77.16659704, "name": "Himachal Pradesh "}, "Jammu And Kashmir ": {"lat": 34.29995933, "lon": 74.46665849, "name": "Jammu And Kashmir "}, "Uttaranchal ": {"lat": 30.32040895, "lon": 78.05000565, "name": "Uttaranchal "}, "Lakshadweep ": {"lat": 10.56257331, "lon": 72.63686717, "name": "Lakshadweep "}, "Goa ": {"lat": 15.491997, "lon": 73.81800065, "name": "Goa "}, "Madhya Pradesh ": {"lat": 21.30039105, "lon": 76.13001949, "name": "Madhya Pradesh "}, "Mizoram ": {"lat": 23.71039899, "lon": 92.72001461, "name": "Mizoram "}, "Tamil Nadu ": {"lat": 12.92038576, "lon": 79.15004187, "name": "Tamil Nadu "}, "Andaman And Nicobar ": {"lat": 11.66702557, "lon": 92.73598262, "name": "Andaman And Nicobar "}, "Maharashtra ": {"lat": 19.25023195, "lon": 73.16017493, "name": "Maharashtra "}, "Dadra And Nagar Haveli ": {"lat": 20.26657819, "lon": 73.0166178, "name": "Dadra And Nagar Haveli "}, "Tripura ": {"lat": 23.83540428, "lon": 91.27999914, "name": "Tripura "}, "Kerala ": {"lat": 8.900372741, "lon": 76.56999263, "name": "Kerala "}, "Arunachal Pradesh ": {"lat": 27.10039878, "lon": 93.61660071, "name": "Arunachal Pradesh "}, "Bihar ": {"lat": 25.78541445, "lon": 87.4799727, "name": "Bihar "}, "Uttar Pradesh ": {"lat": 27.59998069, "lon": 78.05000565, "name": "Uttar Pradesh "}, "Assam ": {"lat": 26.7499809, "lon": 94.21666744, "name": "Assam "}, "Chandigarh ": {"lat": 30.71999697, "lon": 76.78000565, "name": "Chandigarh "}}

    
      
function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 5,
      center: { lat: 20.59, lng: 78.9 },
    });
    var heatmapData = [
        new google.maps.LatLng(37.782, -122.447),
        new google.maps.LatLng(37.782, -122.445),
        new google.maps.LatLng(37.782, -122.443),
        new google.maps.LatLng(37.782, -122.441),
        new google.maps.LatLng(37.782, -122.439),
        new google.maps.LatLng(37.782, -122.437),
        new google.maps.LatLng(37.782, -122.435),
        new google.maps.LatLng(37.785, -122.447),
        new google.maps.LatLng(37.785, -122.445),
        new google.maps.LatLng(37.785, -122.443),
        new google.maps.LatLng(37.785, -122.441),
        new google.maps.LatLng(37.785, -122.439),
        new google.maps.LatLng(37.785, -122.437),
        new google.maps.LatLng(37.785, -122.435)
      ];
      var heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapData
      });
      heatmap.setMap(map);
       
    const infoWindow = new google.maps.InfoWindow();
    // Create the markers.
    Object.keys(locations).forEach((state, i) => {
      let position = {lat:locations[state].lat, lng:locations[state].lon}
      let title = state
      const marker = new google.maps.Marker({
        position,
        map,
        title: `${title}`,
        optimized: false,
      });
      // Add a click listener for each marker, and set up the info window.
      marker.addListener("click", () => {
        infoWindow.close();
        infoWindow.setContent(marker.getTitle());
        infoWindow.open(marker.getMap(), marker);
        //get stats of state at given time
        //display graph from python
        document.getElementById("content").innerHTML = marker.getTitle();
      });
    });
  }
  
document.getElementById("vaccineForm").addEventListener("submit", vaccineSubmit)

function vaccineSubmit(e){
    e.preventDefault()
    if(isNaN(document.getElementById("vaccines").value)){
        window.alert("Please enter a number")
    }
    else{
       //get data from python
       //Make slider
    }
    
}