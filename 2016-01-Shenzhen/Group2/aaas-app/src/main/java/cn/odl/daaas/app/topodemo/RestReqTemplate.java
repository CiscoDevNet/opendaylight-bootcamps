package cn.odl.daaas.app.topodemo;

import java.io.IOException;
import java.io.UnsupportedEncodingException;

import org.apache.http.HttpEntity;
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.Credentials;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.AuthCache;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpEntityEnclosingRequestBase;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.client.methods.HttpRequestBase;
import org.apache.http.client.protocol.HttpClientContext;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.auth.BasicScheme;
import org.apache.http.impl.client.BasicAuthCache;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;


public class RestReqTemplate
{

    public static String doGet(RestReqTempateParam reqTemplateParam)
    {
        String respStr = "";

        HttpRequestBase httprequest = new HttpGet(reqTemplateParam.getRestReqUrl());
        CloseableHttpClient httpclient = HttpClients.createDefault();
        CloseableHttpResponse response = null;
        try
        {
            response = httpclient.execute(httprequest, createBasicAuthContext(reqTemplateParam));
            HttpEntity receivedEntity = response.getEntity();
            if (receivedEntity != null)
            {
                respStr = EntityUtils.toString(receivedEntity);
            }
        }
        catch (ClientProtocolException e)
        {
            System.out.println(e.toString());
        }
        catch (IOException e)
        {
            System.out.println(e.toString());
        }
        finally
        {
            try
            {
                if (null != response)
                {
                    response.close();
                }
                httpclient.close();
            }
            catch (IOException e)
            {
                System.out.println(e.toString());               
            }
        }

        return respStr;
    }

    public static String doPost(RestReqTempateParam reqTemplateParam)
    {
        String respStr = "";

        HttpRequestBase httprequest = new HttpPost(reqTemplateParam.getRestReqUrl());
        StringEntity sentEntity;
        try
        {
            sentEntity = new StringEntity(reqTemplateParam.getEntity(), "utf-8");
            sentEntity.setContentType("application/json");
            ((HttpEntityEnclosingRequestBase) httprequest).setEntity(sentEntity);
        }
        catch (UnsupportedEncodingException e)
        {
            System.out.println(e.toString());
        }

        CloseableHttpClient httpclient = HttpClients.createDefault();
        CloseableHttpResponse response = null;
        try
        {
            response = httpclient.execute(httprequest, createBasicAuthContext(reqTemplateParam));
            HttpEntity receivedEntity = response.getEntity();
            //int httpResponseCode = response.getStatusLine().getStatusCode();
            if (receivedEntity != null)
            {
                respStr = EntityUtils.toString(receivedEntity);
            }
        }
        catch (ClientProtocolException e)
        {
            System.out.println(e.toString());
        }
        catch (IOException e)
        {
            System.out.println(e.toString());
        }
        finally
        {
            try
            {
                if (null != response)
                {
                    response.close();
                }
                httpclient.close();
            }
            catch (IOException e)
            {
                System.out.println(e.toString());               
            }
        }

        return respStr;
    }

    public static String doPut(RestReqTempateParam reqTemplateParam)
    {
        String respStr = "";

        HttpRequestBase httprequest = new HttpPut(reqTemplateParam.getRestReqUrl());
        StringEntity sentEntity;
        try
        {
            sentEntity = new StringEntity(reqTemplateParam.getEntity(), "utf-8");
            sentEntity.setContentType("application/json");
            //sentEntity.setContentEncoding(req.getCharacterEncoding());
            ((HttpEntityEnclosingRequestBase) httprequest).setEntity(sentEntity);
        }
        catch (UnsupportedEncodingException e)
        {
            System.out.println(e.toString());
        }

        CloseableHttpClient httpclient = HttpClients.createDefault();
        CloseableHttpResponse response = null;
        try
        {
            response = httpclient.execute(httprequest, createBasicAuthContext(reqTemplateParam));
            HttpEntity receivedEntity = response.getEntity();
            if (receivedEntity != null)
            {
                respStr = EntityUtils.toString(receivedEntity);
            }
        }
        catch (ClientProtocolException e)
        {
            System.out.println(e.toString());
        }
        catch (IOException e)
        {
            System.out.println(e.toString());
        }
        finally
        {
            try
            {
                if (null != response)
                {
                    response.close();
                }
                httpclient.close();
            }
            catch (IOException e)
            {
                System.out.println(e.toString());               
            }
        }

        return respStr;
    }

    private static HttpClientContext createBasicAuthContext(RestReqTempateParam reqTemplateParam)
    {
        CredentialsProvider credsProvider = new BasicCredentialsProvider();
        Credentials defaultCreds =
                new UsernamePasswordCredentials(reqTemplateParam.getUsername(), reqTemplateParam.getPassword());
        credsProvider.setCredentials(new AuthScope(reqTemplateParam.getOdlHost(), reqTemplateParam.getOdlPort()),
                defaultCreds);

        AuthCache authCache = new BasicAuthCache();
        BasicScheme basicAuth = new BasicScheme();
        authCache.put(new HttpHost(reqTemplateParam.getOdlHost(), reqTemplateParam.getOdlPort()), basicAuth);

        HttpClientContext context = HttpClientContext.create();
        context.setCredentialsProvider(credsProvider);
        context.setAuthCache(authCache);
        return context;
    }

}
