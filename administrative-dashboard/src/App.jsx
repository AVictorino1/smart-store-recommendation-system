import Header from './components/Header/Header.jsx'
import Footer from './components/Footer/Footer.jsx'
import Card from './components/Card/Card.jsx'
import Products from './components/Products_table/Products.jsx'
import Button from './components/Button/Button.jsx'
import SearchBar from './components/SearchBar/SearchBar.jsx'
import styles from './App.module.css'
import NewProductButton from './components/NewProductButton/NewProductButton.jsx'
function App() {
  const products =[{id: 1, name: "Camisa", price: 20},
            {id: 2, name:"Pantalon", price: 40}];
  return(
    <>
      <Header/>
      
      <div className={styles.mainContent}>
        <p className={styles.bienvenido}>¡Bienvenido Usuario!</p>
        <Products items={products} category = "Ropa"/>
        <Footer/>
      </div>
    </>
  );
  }

export default App