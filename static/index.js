// configuration(환경설정)
const apiUrl = document.location.href.startsWith('http://localhost')
  ? 'http://localhost:5000'
  : '';

const range = async ({start, end}) => {
  try { //서버로 정보를 보낸다
    const response = await axios({
        url: `${apiUrl}/range`,
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        data: {
          start, 
          end
        },
    });
    if(response.statusText !== 'OK') {
        throw new Error(response.data.message);
    }  
    return response.data;
  } catch(err) {
    return { error : err.response.data.message || err.message }
  }
}

document.getElementById('submit-form').addEventListener('submit', async(e) => {
  e.preventDefault();
  const data = await range({
    start: document.getElementById('start').value,
    end: document.getElementById('end').value
  })
  console.log(data)
});

