// import { useState, useEffect, useCallback } from "react"; // incorrecto

async function sendHttpRequest(url, config) {
    const response = await fetch(url, config);
    const resData = await response.json();

    if (!response.ok) {
        throw new Error(resData.message || 'Something went wrong, failed to send request');
    };
    return resData;
}

export default function useHttp(url, config, initialData) {
    const [data, setData] = useState(initialData);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState();

    function clearData(){
        setData(initialData); 
    }

    const sendRequest = useCallback(
        async () => { 
            setIsLoading(true);
            try {
                const resData = await sendHttpRequest(url, config); 
                setData(resData);
            } catch (err) {
                setError(err.message || 'Something went wrong.'); 
            }
            setIsLoading(false);
        }, [url, config]); 

    useEffect(() => {
        if ((config && (config.method === 'get' || !config.method)) || !config) { //mistake -> correcto
            sendRequest();
        }
    }, [sendRequest, config]);

    return {
        data,
        isLoading,
        error,
        clearData,
        sendRequest
    }
}