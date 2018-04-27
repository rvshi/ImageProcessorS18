import axios from 'axios';

const baseURL = 'http://vcm-4141.vm.duke.edu:5000';

export const req = (path, body, cb) => {
  axios.post(baseURL + '/' + path, body)
    .then((response) => {
      cb(response);
    })
    .catch((error) => {
      cb(error);
    });
}