/*
 * Cisco Systems, Inc. and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.hack.impl;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.concurrent.Future;

import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hack.rev150105.HackService;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hack.rev150105.StartHackInput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hack.rev150105.StartHackOutput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hack.rev150105.StartHackOutputBuilder;
import org.opendaylight.yangtools.yang.common.RpcResult;
import org.opendaylight.yangtools.yang.common.RpcResultBuilder;

public class HackImpl implements HackService {

	@Override
	public Future<RpcResult<StartHackOutput>> startHack(StartHackInput input) {
		StartHackOutputBuilder startHackBuilder=new StartHackOutputBuilder();
		try{
			Process pr = Runtime.getRuntime().exec("python /home/chuck/hack.py");
			BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));
			String line=in.readLine();
			in.close();
			pr.waitFor();
			startHackBuilder.setResult("success");
		}catch(Exception e){
			startHackBuilder.setResult("failure");
			e.printStackTrace();
		}
		return RpcResultBuilder.success(startHackBuilder.build()).buildFuture();
	}

}
