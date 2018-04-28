import axios from 'axios';

const baseURL = 'https://vcm-4141.vm.duke.edu';

export const req = (jwt, path, body, cb) => {
  if (jwt) {
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + jwt;
  }
  axios.post(baseURL + '/' + path, body)
      .then((response) => {
        cb(response, true);
      })
      .catch((error) => {
        cb(error, false);
      });
};


export const validate = (jwt, cb) => {
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + jwt;
  axios.get(baseURL + '/validate')
      .then((response) => {
        cb(response, true);
      })
      .catch((error) => {
        cb(error, false);
      });
};