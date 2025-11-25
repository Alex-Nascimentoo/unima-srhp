'use client'

import { Product } from '@/app/_types/product'
import React, { useEffect } from 'react'
import api from '../../lib/axios'
import { Category } from '@/app/_types/category'
import { CurrencyInput } from 'react-currency-mask'

type Props = {
  isOpen: boolean
  setIsOpen: (isOpen: boolean) => void
  fetchProducts: () => Promise<void>
}

function AddProductPopup(props: Props) {
  const [newProduct, setNewProduct] = React.useState<Product>({
    id: 0,
    name: '',
    key: '',
    price: 0,
    id_category: 0,
  })
  const [categoryList, setCategoryList] = React.useState<Category[]>([])

  function closePopup() {
    setNewProduct({
      id: 0,
      key: '',
      name: '',
      price: 0,
      id_category: 0,
    })
    props.setIsOpen(false)
  }

  async function handleAddProduct(e: React.FormEvent) {
    e.preventDefault()

    // Here you would typically send newProduct to your backend API
    console.log('Adding product:', newProduct)
    try {
      const { id: _, ...productDto } = newProduct // Exclude id when sending to backend
      const response = await api.post('/business/product/add', productDto)
      console.log('Product added successfully:', response.data)
    } catch (error) {
      console.error('Error adding product:', error)
    }

    // Reset form and close popup
    closePopup()
    await props.fetchProducts(); // Call the function to update the product list in the parent component
  }

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await api.get('/business/category')
        console.log('Categories fetched:', response.data)
        setCategoryList(response.data)
      } catch (error) {
        console.error('Error fetching categories:', error)
      }
    }

    fetchCategories()
  }, [])

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
            Adicionar Produto
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
            value={newProduct.name}
            onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
          />

          <label
            className="
            font-semibold
            "
          >
            Preço do Produto:
          </label>
          <CurrencyInput
            value={newProduct.price}
            onChangeValue={(_, value) => {
              const numericValue = value ? parseFloat(value as string) : 0
              setNewProduct({ ...newProduct, price: numericValue })
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
            value={newProduct.id_category}
            onChange={(e) => setNewProduct({ ...newProduct, id_category: parseInt(e.target.value) })}
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
            onClick={handleAddProduct}
          >
            Adicionar Produto
          </button>
        </form>
      </div>
    </div>
  )
}

export default AddProductPopup