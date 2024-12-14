import { defineEventHandler, readBody, createError } from 'h3'
import { useRuntimeConfig } from '#imports'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { token } = body
  const config = useRuntimeConfig()

  if (!token) {
    throw createError({
      statusCode: 400,
      message: 'No token provided'
    })
  }

  try {
    // Verify token with FastAPI backend
    const response = await $fetch(`${config.public.apiUrl}/api/v1/login/test-token`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    // If token is valid, return it to be stored in auth store
    return {
      token,
      user: response
    }
  } catch (error) {
    throw createError({
      statusCode: 401,
      message: 'Invalid or expired token'
    })
  }
})
