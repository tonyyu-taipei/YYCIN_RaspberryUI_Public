// download the medication api data from the server
// store json data into assets/medication.json
// provide some methods to get the data from the parameter(color, shape, imprint)
// and return the result to the caller
//
import axios from 'axios';
import { apiBaseUrl } from '../api';
let med_url = apiBaseUrl+"medication";

let med_data = await axios.get(med_url);
console.log(med_data.data);

export function getColor(color){
    let result = [];
    med_data.data.forEach((item)=>{
        if(item.color === color){
            result.push(item);
        }
    });
    return result;
}
