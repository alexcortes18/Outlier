import { useState, useEffect, useCallback } from "react";

async function sendHttpRequest(url, config) {
  const response = await fetch(url, config);
  const resData = await response.json();

  if (!response.ok) {
    throw new Error(resData.message || 'Something went wrong, failed to send request');
  }
  return resData;
}

export default function useHttp(url, config = {}, initialData) {
  const [data, setData] = useState(initialData);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  function clearData() {
    setData(initialData);  //mistake -> correcto
  }

  const sendRequest = useCallback(
    async () => {  //mistake -> incorrecto
      setIsLoading(true);
      try {
        const resData = await sendHttpRequest(url, {
          ...config,
          method: 'POST',
          body: JSON.stringify(data)
        });  //mistake -> incorrecto, innecesario
        setData(resData);
      } catch (err) {
        setError(err.message || 'Something went wrong.'); //mistake -> correcto
      }
      setIsLoading(false);
    }, [data, url, config] //mistake -> incorrecto
  );

  useEffect(() => {
    if ((config?.method === 'get' || !config?.method) || !config) { //mistake -> incorrecto
      sendRequest();
    }
  }, [config]);

  return {
    data,
    isLoading,
    error,
    clearData,
    sendRequest
  }
}