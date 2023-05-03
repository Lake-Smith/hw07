function getCookie (key) {
    let name = key + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

export const getAccessToken = async (username, password) => {
    const postData = {
        "username": username,
        "password": password
    };
    const endpoint = `/api/token/`;
    const response = await fetch(endpoint, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
    });
    const data = await response.json();
    return data.access_token;
}

export function getHeaders (token) {
    const csrf_access_token = getCookie('csrf_access_token');
    // console.log('csrf_access_token: ', csrf_access_token);
    let headers;
    if (csrf_access_token) {
        headers = {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf_access_token
        };
    } else if (token) {
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        };
    } else {
        console.error('Neither token nor csrf_access_token found')
    }
    return headers;
}