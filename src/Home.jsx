import React , {useState , useEffect} from 'react'
import Banner from './Banner';
import   './css/home.css';
import Footer from './Footer';

export default function Home() {
    const [data, setData] = useState([{}]);

    useEffect(() =>{
        fetch("/preds").then(
            res => res.json()
            
            ).then(
            data => {
                setData(data)
            console.log(data)
            })
    },[])


    const handlePredict= () =>{

        // alert("hello " + data.name)
    }
    return (
        <div className='home'>
            <Banner/>

{/* <p className='par'> <a href=' https://www.kaggle.com/datasets/skillsmuggler/amazon-ratings#https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews
'> datatse link</a></p> */}
<p>Here are the  10 products recommended based on user ratings. The products are in  with the item purchased by a particular  customer based on items rated by 
    other customers  who bought the same product say the product with the product id
    '1304624498' and outputs other products recommendation in Correlation with other products other users rated
</p>
<hr></hr>
<p> Here are the 10 products represented by  their  id's...</p>
{(typeof data.predictions === 'undefined')?(
    <p>Loading ...</p>
): 
 (data.predictions?.map((predictions, i)=>(
    <h6 id= "list" key={i}>product   {i + "=>"}: {predictions}</h6>
 ))
 )}

 

    <Footer/>
        </div>

        
    )
}
