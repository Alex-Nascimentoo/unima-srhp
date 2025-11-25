'use client'

import { useEffect, useState } from 'react';
import api from '../lib/axios';
import { Product } from '../_types/product';
import AddProductPopup from './_components/addProduct';
import { Category } from '../_types/category';
import ViewProductPopup from './_components/viewProductPopup';

export default function PublicBusinessPage() {
  const [productList, setProductList] = useState<Product[]>([]);
  const [categoryList, setCategoryList] = useState<Category[]>([]);
  const [isAddProductOpen, setIsAddProductOpen] = useState(false);
  const [isViewProductOpen, setIsViewProductOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product>({} as Product);
  const [searchTerm, setSearchTerm] = useState('');

  async function deleteProdcut(key: string) {
    try {
      const response = await api.delete(`/business/product/delete/${key}`);
      console.log('Product deleted successfully:', response.data);
      // Optionally, refresh the product list after deletion
      setProductList(productList.filter(product => product.name !== key));
    } catch (error) {
      console.error('Error deleting product:', error);
    }
  }

  async function fetchProducts() {
    try {
      const response = await api.get('/business/product');
      setProductList(response.data);
      setSelectedProduct(response.data[0] || {} as Product);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  }

  useEffect(() => {
    // Fetch data or perform actions on mount
    const fetchData = async () => {
      try {
        const response = await api.get('/business/product');
        const categoryResponse = await api.get('/business/category');
        
        setProductList(response.data);
        setSelectedProduct(response.data[0] || {} as Product);
        setCategoryList(categoryResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);
  
  return (
    <main
      className="
      w-full h-full
      bg-gray-300
      text-black
      "
    >
      <AddProductPopup
        isOpen={isAddProductOpen}
        setIsOpen={setIsAddProductOpen}
        fetchProducts={fetchProducts}
      />

      <ViewProductPopup
        isOpen={isViewProductOpen}
        setIsOpen={setIsViewProductOpen}
        currentProduct={selectedProduct}
        fetchProducts={fetchProducts}
      />

      <section
        className="
        max-w-[1080px] mx-auto pt-15
        "
      >

        <div>
          <input
            type="text"
            placeholder="Buscar produto..."
            className="
            w-full
            p-3 px-5
            rounded-md
            mt-10 mb-5
            border border-gray-400
            bg-white
            font-semibold text-black
            focus:outline-none focus:border-gray-600
            shadow-lg
            "
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div
          className="
          flex justify-between items-center
          "
        >
          <h1
            className="
            font-bold text-3xl
            "
          >Produtos</h1>

          <button
            className="
            bg-gray-800
            text-white font-bold
            px-3 py-1
            rounded-md

            duration-200

            hover:bg-white
            hover:text-black
            hover:cursor-pointer
            "
            onClick={() => setIsAddProductOpen(!isAddProductOpen)}
          >Adicionar</button>
        </div>

        <hr
          className="
          mt-3
          text-gray-400
          "
        ></hr>


        <div
          className="
          grid grid-cols-9
          mt-7 px-3 py-1
          bg-gray-800
          rounded-md
          font-bold text-white
          "
        >
          <p
            className="
            col-span-5
            "
          >Nome</p>
          <p
            className="
            col-span-2
            text-right
            pr-20
            "
          >Valor</p>
          <p
            className="
            col-span-2
            text-center
            "
          >Ações</p>
        </div>

        <div
          className="
          flex flex-col gap-y-2
          h-[420px] mb-10 pb-2
          rounded-lg
          shadow-2xl
          overflow-y-scroll
          bg-gray-400
          "
        >
          {
            productList
              .filter(product => 
                product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                categoryList.find(c => c.id === product.id_category)?.name.toLowerCase().includes(searchTerm.toLowerCase())
              )
              .map((product, idx) => {
              const categoryName = categoryList.find(c => c.id === product.id_category)?.name || 'Categoria não encontrada';
              
              return (
                <div
                  key={product.id}
                  className={`
                  grid grid-cols-9 items-center
                  px-3 py-2
                  ${idx % 2 === 0 ? 'bg-gray-200' : 'bg-white'}
                  rounded-md
                  font-bold
                  `}
                >
                  <div
                    className="
                    col-span-5
                    "
                  >
                    <h2>{product.name}</h2>
                    <p
                      className="
                      font-normal text-gray-600
                      "
                      
                    >{categoryName}</p>
                  </div>

                  <p
                    className="
                    col-span-2
                    text-right
                    pr-15
                    "
                  >R$ {
                    product.price.toLocaleString('pt-BR', {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })
                    }
                  </p>

                  <div
                    className="
                    col-span-2
                    flex justify-center items-center gap-x-3
                    "
                  >
                    <button
                      className="
                      bg-red-600
                      text-white font-bold
                      px-3 py-1
                      rounded-md

                      duration-200

                      hover:bg-red-800
                      hover:cursor-pointer
                      "
                      onClick={() => deleteProdcut(product.name)}
                    >
                      Deletar
                    </button>
                    
                    <button
                      className="
                      bg-blue-600
                      text-white font-bold
                      px-3 py-1
                      rounded-md

                      duration-200

                      hover:bg-blue-800
                      hover:cursor-pointer
                      "
                      onClick={() => {
                        setIsViewProductOpen(true)
                        setSelectedProduct(product)
                        console.log('selected product: ', selectedProduct)
                      }}
                    >
                      Ver
                    </button>


                  </div>
                </div>
              )
            })
          }
        </div>
      </section>
    </main>
  )
}
