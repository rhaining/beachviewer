function loadRemoteDoc(url, completion) {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
           if (xmlhttp.status == 200) {
             completion(xmlhttp.responseText)
               // document.getElementById("myDiv").innerHTML = xmlhttp.responseText;
           } else {
             document.getElementById("loading-indicator").style.display = "none";
           }
           // else if (xmlhttp.status == 400) {
              // alert('There was an error 400');
           // }
           // else {
               // alert('something else other than 200 was returned');
           // }
        }
    };

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function get_house_row(house) {
  var buffer = "<tr>\n"

  buffer += "\t<td>" + house["rentalAgency"] + "</td>\n"

  buffer += "\t<td>"
  // if(house["image"].length > 0) {
    var image_url = house["image"]
    buffer += "<a href=\"" + image_url + "\" target=\"_blank\"><img data-src=\""
            + image_url + "\" class=\"lozad\"/></a>"
  // }
  buffer += "\t</td>"

  buffer += "\t<td>" + house["name"] + "</td>"

  buffer +=  "\t<td>"
          + house["regionName"]
          + " [<a href=\"" + house["mapURL"] + "\" target=_blank>map it</a>] "
          + " [<a href=\"" + house["nearbyURL"] + "\">nearby</a>] "
          + "</td>"

  buffer += "<td><div class=\"oceanfront\">" + house["oceanfront"] + "</div></td>"

  buffer += "<td>" + house["cost"] + "</td>"
  buffer += "<td>" + house["bedrooms"] + " bed / " + house["bathrooms"] + " bath</td>"
  buffer += "<td>" + house["costPerBed"] + "</td>"

  buffer += "<td><a href=\"" + house["url"] + "\" target=_blank>" + house["truncatedURL"] + "</a></td>"

  for(var i=0; i < house["availability"].length; i++) {
    var avail = house["availability"][i]
    if(avail == "none") {
      buffer += "<td><div class=\"unknown_cost\">Not set</div></td>"
    } else {
      buffer += "<td>" + avail + "</td>"
    }
  }
  // buffer += "<td>{{ datetime.datetime.fromtimestamp(BeachTime.seconds_since_2000() + house.get("updatedOn")).strftime("%b %-d, %Y") }} </td>


  buffer += "</tr>\n"
  return buffer
  // document.getElementById("tbody").innerHTML += buffer
}
