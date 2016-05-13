package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hack.rev150105;
import org.opendaylight.yangtools.yang.binding.RpcService;
import org.opendaylight.yangtools.yang.common.RpcResult;
import java.util.concurrent.Future;


/**
 * Interface for implementing the following YANG RPCs defined in module &lt;b&gt;hack&lt;/b&gt;
 * &lt;br&gt;(Source path: &lt;i&gt;META-INF/yang/hack.yang&lt;/i&gt;):
 * &lt;pre&gt;
 * rpc start-hack {
 *     input {
 *         leaf time {
 *             type string;
 *         }
 *     }
 *     
 *     output {
 *         leaf result {
 *             type string;
 *         }
 *     }
 *     status CURRENT;
 * }
 * &lt;/pre&gt;
 *
 */
public interface HackService
    extends
    RpcService
{




    Future<RpcResult<StartHackOutput>> startHack(StartHackInput input);

}

