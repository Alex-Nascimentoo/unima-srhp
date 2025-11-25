'use client'

import { Category } from '@/app/_types/category'
import { Product } from '@/app/_types/product'
import api from '@/app/lib/axios'
import { useEffect, useState } from 'react'
import { CurrencyInput } from 'react-currency-mask'

type Props = {
  isOpen: boolean
  setIsOpen: (isOpen: boolean) => void
  currentProduct: Product
  fetchProducts: () => Promise<void>
}

function ViewProductPopup(props: Props) {

  const [product, setProduct] = useState<Product>(props.currentProduct)
  const [categoryList, setCategoryList] = useState<Category[]>([])
  const [recommendationList, setRecommendationList] = useState<{
    key: string
    product: Product
  }[]>([])

  function closePopup() {
    setProduct({
      id: 0,
      key: '',
      name: '',
      price: 0,
      id_category: 0,
    })

    props.setIsOpen(false)
  }

  async function handleEditProduct(e: React.FormEvent) {
    e.preventDefault()

    // Here you would typically send updated product to your backend API
    console.log('Editing product:', product)
    try {
      const response = await api.put(`/business/product/update/${product.key}`, product)
    } catch (error) {
      console.error('Error editing product:', error)
    }

    // Close popup
    closePopup()
    await props.fetchProducts(); // Call the function to update the product list in the parent component
  }

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await api.get('/business/category')
        setCategoryList(response.data)
      } catch (error) {
        console.error('Error fetching categories:', error)
      }
    }

    async function fetchRecommendations() {
      try {
        const response = await api.get(`/business/product/recommend?key=${product.key}`)
        console.log('recommendation list: ', response.data)
        setRecommendationList(response.data)
      } catch (error) {
        console.error('Error fetching recommendations:', error)
      }
    }

    fetchRecommendations()
    fetchCategories()
  }, [product.key])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setProduct(props.currentProduct)
  }, [props.currentProduct])
  
  return (
    <div
      className={`
      absolute top-0 left-0 ${props.isOpen ? 'flex' : 'hidden'}
      w-full h-full
      bg-black/30
      items-center justify-center  
      `}
      onClick={() => closePopup()}
    >
      <div
        className="
        bg-white shadow-2xl
        rounded-lg
        w-[720px] p-5
        relative
        "
        onClick={(e) => e.stopPropagation()}
      >
        <div
          className="
          flex justify-between items-center
          "
        >
          <h2
            className="
            font-bold text-2xl mb-5
            "
          >
            Visualizar Produto
          </h2>
          
          <h2
            className="
            font-bold text-2xl text-red-800
            cursor-pointer
            mb-5

            hover:scale-120
            hover:text-red-500
            duration-200
            "
            onClick={() => closePopup()}
          >
            X
          </h2>
        </div>
        
        <form action="">
          <label
            className="
            font-semibold
            "
          >
            Nome do Produto:
          </label>
          <input
            type="text"
            className="
            w-full
            border border-gray-400
            rounded-md
            p-2
            mt-1 mb-3
            "
            value={product.name}
            onChange={(e) => setProduct({ ...product, name: e.target.value })}
          />

          <label
            className="
            font-semibold
            "
          >
            Preço do Produto:
          </label>
          <CurrencyInput
            value={product.price}
            onChangeValue={(_, value) => {
              const numericValue = value ? parseFloat(value as string) : 0
              setProduct({ ...product, price: numericValue })
            }}
            InputElement={
              <input
                type="text"
                className="
                w-full
                border border-gray-400
                rounded-md
                p-2
                mt-1 mb-3
                "
              />
            }
          />

          <label
            className="
            font-semibold
            "
          >
            Categoria:
          </label>
          <select
            className="
            w-full
            border border-gray-400
            rounded-md
            p-2
            mt-1 mb-5
            "
            value={product.id_category}
            onChange={(e) => setProduct({ ...product, id_category: parseInt(e.target.value) })}
          >
            <option value={0} disabled hidden>Selecione uma categoria</option>
            {
              categoryList.map((category) => (
                <option
                  key={category.id}
                  value={category.id}
                >
                  {category.name}
                </option>
              ))
            }
          </select>

          <button
            className="
            bg-gray-800
            text-white text-xl font-bold
            px-3 py-1
            rounded-md
            float-end

            duration-200

            hover:bg-gray-500
            hover:text-black
            hover:cursor-pointer
            "
            onClick={handleEditProduct}
          >
            Editar Produto
          </button>
        </form>

        {/* other products recommendation section */}
        <div>
          <h3
            className="
            font-bold text-2xl
            mt-10 mb-5
            "
          >Recomendações</h3>
          <div
            className="
            flex gap-4
            overflow-x-scroll
            py-4
            "
          >
            {/* Recommendation items would go here */}
            {recommendationList.map((rec) => (
                <div
                key={rec.key}
                className="
                bg-gray-400
                rounded-xl
                p-2 px-4 w-[180px]
                shadow-xl
                flex flex-col justify-between
                "
                >
                
                <p
                  className="
                  font-bold
                  mb-4
                  "
                >{rec.product.name}</p>
                
                <p
                  className="
                  text-right font-semibold
                  "
                >R$ {rec.product.price.toLocaleString('pt-BR', {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })}</p>
                </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  )
}

export default ViewProductPopup