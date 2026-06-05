'use strict';
const apiBaseUrl = "http://localhost:8000/api";

class DataManager {
   

    async promptRequest(prompt) {
        const response = await fetch(`${apiBaseUrl}/prompt`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: prompt
            })
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const responseJson = await response.json();
        if(responseJson.answer) {
            responseJson.answer = responseJson.answer.replace(/\n/g, "<br>");
            return Promise.resolve(responseJson);
        }
        return Promise.reject(new Error("Invalid response format"));
    }
}

export default DataManager;