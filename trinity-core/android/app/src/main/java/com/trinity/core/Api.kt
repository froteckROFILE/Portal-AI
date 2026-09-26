package com.trinity.core
import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
data class SolveRequest(val prompt:String, val mode:String="arena")
data class Candidate(val provider:String, val answer:String, val ok:Boolean, val error:String?)
data class SolveResponse(val final:String, val candidates:List<Candidate>, val audit:Map<String,Any>)
interface TrinityApi { @POST("solve") suspend fun solve(@Body request:SolveRequest):SolveResponse }
object Api { val service: TrinityApi = Retrofit.Builder().baseUrl(BuildConfig.API_BASE_URL).addConverterFactory(GsonConverterFactory.create()).build().create(TrinityApi::class.java) }
