import { useState } from "react";

function App() {
  const [url,setUrl]=useState('')
  const [result,setResult]=useState('')


  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:5000', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({url})
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data['out'])
        console.log(data); 
      } else {
        console.error('Failed to fetch'); 
      }
    } catch (error) {
      console.error('Error:', error); 
    }
  };



  return (
    <div className="header_section">
         <div className="banner_section layout_padding">
            <div id="my_slider" className="carousel slide" data-ride="carousel">
               <div className="carousel-inner">
                  <div className="carousel-item active">
                     <div className="container">
                        <div className="row back_graound" >
                           <div className="col-md-6">
                              <div className="taital_main text_place">
                                 <h4 className="banner_taital">Anti Phishing</h4>
                                 <p className="banner_text">This website utilizes artificial intelligence to determine whether a website is engaged in phishing activities or not.</p>
                                 
                              </div>
                           </div>
                
                           <div className="col-md-6">
                              <div><img src="images/img_1.gif" className="image_1"/></div>
                           </div>
                        </div>
                        
                        <div className="button_main">
                          <input 
                            value={url}
                            type="text" 
                            className="Enter_text" 
                            placeholder="Enter Url"
                            onChange={e=>{
                              setUrl(e.target.value)
                              setResult('')
                            }}
                            />
                          <button 
                            className="search_text"
                            onClick={handleSubmit}
                          >
                            Verify
                          </button>
                        </div>

                        {result!==''?(<>
                            {result!=='true'?(
                              <div className="row back_graound " style={{ color: "red", textAlign: "center" }} ><h4 className="banner_taital">Phising</h4></div>
                            ):(
                              <div className="row back_graound " style={{ color: "green", textAlign: "center" }}  ><h4 className="banner_taital">Legitimate</h4></div>
                            )
                          }  
                        </>):(<></>)}
                     </div>
                  </div>
               </div>
            </div>
         </div>
      </div>
  );
}

export default App;
