import {useState, useEffect} from "react"
import styles from './Products.module.css'
import Dropdown from "../Dropdown/Dropdown.jsx"
import {FaPen} from "react-icons/fa"
import { BsPencilSquare } from "react-icons/bs";
import EditModal from "../EditProductModal/EditProductModal";

const orderOptions = [
        {label: "A-Z ", value : "ALPHA"},
        {label: "Z-A ", value : "REVERSE"},
        {label: "Precio menor ", value : "ASCEN"},
        {label: "Precio mayor", value : "DESCEN"},

    ]



function Products({category="Category", filter="all"}){
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const[error, setError] = useState(null);
    const [order, setOrder] = useState("ALPHA");
    const [showModal, setShowModal] = useState(false);
    const [selectedProduct, setSelectedProduct] = useState(null);


    useEffect(() => {
        fetch("http://localhost:8000/products")
        .then(res => {
            if (!res.ok) throw new Error("Error al obtener productos")
            return res.json()        
        }
        )

        .then(data => {
            setProducts(data)
            setLoading(false)
        })
        .catch(err => {
            setError(err.message)
            setLoading(false)
        })


    }, [])
    let processed = [...products]

    
    switch(order){
        case "ALPHA":
            processed.sort((a,b) => (a.name || "").localeCompare(b.name || ""));
            break;
        case "REVERSE":
            processed.sort((a,b) => (b.name || "").localeCompare(a.name || ""));
            break;
        case "ASCEN":
            processed.sort((a,b) => a.price - b.price);
            break;
        case "DESCEN":
            processed.sort((a,b) => b.price - a.price);
            break;
    };

    switch(filter){
        case "PRICE":
            processed = processed.filter(product => product.price <= 30);
            break;
            
        default:
            break;
    };

    useEffect(() => {
        if (showModal){
            document.body.style.overflow = "hidden";
        }
        else{
            document.body.style.overflow = "";
        }

         return () => {
        document.body.style.overflow = ""
        }
    }, [showModal])
    if (loading) return <p> Cargando productos...</p>
    if (error) return <p>Erro: {error}</p>


    

    return (<>
    {showModal && <EditModal close={() => setShowModal(false)} product={selectedProduct}></EditModal>}
    
    <br></br>
    <div className = {styles.divtabla}>
        <Dropdown  label="Ordenar" options={orderOptions} onSelect={setOrder} className ={styles.filtrosd}></Dropdown>
        <table className={styles.products}>
            <thead>
                <tr className={styles.columnsNames}>
                    <th className={styles.th}>ID</th>
                    <th className={styles.th}>Nombre</th>
                    <th className={styles.th}>Categoría</th>
                    <th className={styles.th}>Subcategoría</th>
                    <th className={styles.th}>Precio</th>
                    <th className={styles.th}>Marca</th>
                    <th className={styles.th}>Color</th>
                    <th className={styles.th}>Description</th>
                    <th className={styles.th}></th>

                </tr>
            </thead>
            
            <tbody>
                {processed.map(product => (
                    <tr className={styles.row} key={product.id}>
                        <td className={styles.td}>{product.id}</td>
                        <td className={styles.td}>{product.name}</td>
                        <td className={styles.td}>{product.category}</td>
                        <td className={styles.td}>{product.subcategory}</td>
                        <td className={styles.td}>{product.price}</td>
                        <td className={styles.td}>{product.brand}</td>
                        <td className={styles.td}>{product.color}</td>
                        <td className={styles.td}>{product.description}</td>
                        <td className={styles.action}><BsPencilSquare className={styles.edit} onClick = {() => {setSelectedProduct(product); setShowModal(true); }}/></td>
                        
                    
                    </tr> 
                ))}
            </tbody>
        </table>
    </div>
    <br></br>
    </>);
}


export default Products