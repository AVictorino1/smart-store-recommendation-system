import { useState, useEffect } from "react"
import styles from './Products.module.css'
import { BsPencilSquare, BsArrowDownUp, BsFunnel } from "react-icons/bs";
import EditModal from "../EditProductModal/EditProductModal";
import { FaWhatsapp, FaInstagram, FaFacebook, FaTiktok } from "react-icons/fa";

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
    const [expandedDescriptions, setExpandedDescriptions] = useState([])
    const [selectedIds, setSelectedIds] = useState([]);
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

    function toggleSelect(id) {
    setSelectedIds(prev =>
        prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
    }

    function toggleSelectAll() {
        if (selectedIds.length === processed.length) {
            setSelectedIds([]);
        } else {
            setSelectedIds(processed.map(p => p.id));
        }
    }

    const isAllSelected = processed.length > 0 && selectedIds.length === processed.length;

    function toggleDescriptions(id){
        setExpandedDescriptions(prev => (prev.includes(id) ? prev.filter(x => x !== id):  [...prev, id]));
    }

    function updateProduct(updated){
        setProducts(products.map(p => p.id === updated.id ? updated: p));
        setSelectedProduct(updated);
    }
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
    {showModal && <EditModal onSave={updated => {updateProduct(updated);}} close={() => setShowModal(false)} product={selectedProduct}></EditModal>}
    
    <br></br>
    <div className={styles.divtabla}>

        <div className={styles.topRow}>
            <div className={styles.filterTabs}>
                <button className={`${styles.tabButton} ${styles.tabButtonActive}`}>Todos</button>
                <button className={styles.tabButton}>Publicados</button>
                <button className={styles.tabButton}>Reservados</button>
                <button className={styles.tabButton}>Vendidos</button>
            </div>

            <div className={styles.rightControls}>
                {selectedIds.length > 0 && (
                    <span className={styles.selectionCount}>{selectedIds.length} seleccionado(s)</span>
                )}

                <div className={styles.publishWrapper}>
                    <button className={styles.publishButton} disabled={selectedIds.length === 0}>
                        <FaWhatsapp className={styles.channelIcon} />
                        <FaInstagram className={styles.channelIcon} />
                        <FaFacebook className={styles.channelIcon} />
                        <FaTiktok className={styles.channelIcon} />
                        <span>Publicar</span>
                    </button>

                    {selectedIds.length === 0 && (
                        <span className={styles.publishTooltip}>
                            Debe seleccionar al menos un producto para publicar
                        </span>
                    )}
                </div>

                <div className={styles.toolbar}>
                    <button className={styles.iconButton} title="Ordenar">
                        <BsArrowDownUp />
                    </button>
                    <button className={styles.iconButton} title="Filtros">
                        <BsFunnel />
                    </button>
                </div>
            </div>
        </div>

        <div className={styles.tableCard}>
            <table className={styles.products}>
                <thead>
                    <tr className={styles.columnsNames}>
                        <th className={`${styles.thCheckbox} ${styles.th}`}>
                            <input
                                type="checkbox"
                                checked={isAllSelected}
                                onChange={toggleSelectAll}
                            />
                        </th>
                        <th className={styles.th}></th>
                        <th className={styles.th}>Nombre</th>
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
                            <td className={styles.tdCheckbox}>
                                <input
                                    type="checkbox"
                                    checked={selectedIds.includes(product.id)}
                                    onChange={() => toggleSelect(product.id)}
                                />
                            </td>
                            <td className={styles.td}>
                                <img className={styles.image_logo} src={product.image_url}>
                                </img>
                                </td>
                            <td className={styles.td}>{product.name}</td>
                            <td className={styles.td}>{product.price}</td>
                            <td className={styles.td}>{product.brand}</td>
                            <td className={styles.td}>{product.color}</td>
                            <td className={styles.td}>
                                    <div className={styles.descriptionCell}>
                                        {expandedDescriptions.includes(product.id) ? (
                                            <>
                                                <span className={styles.descriptionFull}>{product.description}</span>
                                                <button className={styles.descToggle} onClick={() => toggleDescriptions(product.id)}>
                                                    Mostrar menos
                                                </button>
                                            </>
                                        ) : (
                                            <>
                                                <span className={styles.descriptionTruncated}>{product.description}</span>
                                                <button className={styles.descToggleHover} onClick={() => toggleDescriptions(product.id)}>
                                                    Mostrar todo
                                                </button>
                                            </>
                                        )}
                                    </div>
                                </td>
                            <td className={styles.action}><BsPencilSquare className={styles.edit} onClick={() => {console.log("CLICK DETECTADO"); setSelectedProduct(product); setShowModal(true); }}/></td>
                        </tr> 
                    ))}
                </tbody>
                
            </table>
        </div>

    </div>
    <br></br>
    </>);
}


export default Products