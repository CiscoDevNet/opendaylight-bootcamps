package cn.odl.daaas.app.topodemo;

public class RestReqTempateParam
{
    private String restReqUrl;
    
    private String entity;
    
    private String username;
    
    private String password;
    
    private String odlHost;
    
    private int odlPort;
    
    public String getRestReqUrl()
    {
        return restReqUrl;
    }

    public void setRestReqUrl(String restReqUrl)
    {
        this.restReqUrl = restReqUrl;
    }

    public String getEntity()
    {
        return entity;
    }

    public void setEntity(String entity)
    {
        this.entity = entity;
    }

    public String getUsername()
    {
        return username;
    }

    public void setUsername(String username)
    {
        this.username = username;
    }

    public String getPassword()
    {
        return password;
    }

    public void setPassword(String password)
    {
        this.password = password;
    }

    public String getOdlHost()
    {
        return odlHost;
    }

    public void setOdlHost(String odlHost)
    {
        this.odlHost = odlHost;
    }

    public int getOdlPort()
    {
        return odlPort;
    }

    public void setOdlPort(int odlPort)
    {
        this.odlPort = odlPort;
    }

  
}
