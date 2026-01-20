
// Imports
import React, { useState, useEffect } from "react";
import Chart from "chart.js/auto";
import { Line } from "react-chartjs-2";
import useWebSocket, { ReadyState } from 'react-use-websocket';
import './App.css'

// Synchronous implementation
function httpGet(theUrl) {
  var xmlHttp = new XMLHttpRequest();

  xmlHttp.open("GET", theUrl, false); // false for synchronous request    
  xmlHttp.send();

  return xmlHttp.responseText;
}


function App() {



  const [flag, setFlag] = useState(false);
  const [intervalId, setIntervalId] = useState(0);
  const [repetitions, setRepetitions] = useState(0);
  const [socketUrl, setSocketUrl] = useState('wss://bpcy4gu0ld.execute-api.us-east-1.amazonaws.com/production/');
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);

  const [data, setData] = useState({
    labels: [],
    datasets: [
      {
        label: "ESP32 Temperature",
        backgroundColor: "rgb(255, 99, 132)",
        borderColor: "rgb(255, 99, 132)",
        data: [],
      },
      {
        label: "ESP32 Humidity",
        backgroundColor: "rgb(132,99,255)",
        borderColor: "rgb(132, 99, 255)",
        data: [],
      }
    ],
  });

  useEffect(() => {
    const paragraph1 = document.getElementById('paragraph1');
    paragraph1.innerText = `Number of repetitions: ${repetitions}`;
    
  },[repetitions]);

  useEffect(() => {
    if(lastMessage!=null){
    const paragraph2 = document.getElementById('paragraph2');
    paragraph2.innerText = 'Sensor realtime data: '+lastMessage.data;
    }
  },[lastMessage]);



  const handleClick = () => {

    if (flag == false) {
      const myIntervalID = setInterval(() => {


        const JSONResponse = httpGet("https://3c7e3p7qyh.execute-api.us-east-1.amazonaws.com/production/data");
        const esp32Items = JSON.parse(JSONResponse);


        const tempValues = esp32Items.map((item) => {
          return item.temp;
        });

        const humValues = esp32Items.map((item) => {
          return item.hum;
        });

        const labels = esp32Items.map((item) => {
          const myDate = new Date(item.timestamp);
          return myDate.getDate().toString()
            + "-" + (myDate.getMonth() + 1).toString()
            + "-" + myDate.getFullYear()
            + " " + myDate.getHours()
            + ":" + myDate.getMinutes();
        });




        const myData = {
          labels: labels,
          datasets: [
            {
              label: "ESP32 Humidity",
              backgroundColor: "rgb(255, 99, 132)",
              borderColor: "rgb(255, 99, 132)",
              data: humValues,
            },
            {
              label: "ESP32 Temperature",
              backgroundColor: "rgb(132, 99, 255)",
              borderColor: "rgb(132, 99, 255)",
              data: tempValues,
            }
          ],
        };

        setData(myData);
        // Use functional argument to access previous state
        setRepetitions((prevRepetitions) => { return prevRepetitions + 1 });
        //setRepetitions(repetitions+1);
        console.log(repetitions);

      }, 10000);
      setIntervalId(myIntervalID);
      setFlag(true);
    } else {
      clearInterval(intervalId);
      setFlag(false);

    }

  }

  return (
    <div>
      <div id="buttondiv">
        <button id="button1" onClick={handleClick}> {flag ? "Stop" : "Start"} </button>
      </div>
      <p id="paragraph1"></p>
      <div>
      <p id="paragraph2"></p>
      </div>
      <Line data={data} />
    </div>

  );
}
export default App;